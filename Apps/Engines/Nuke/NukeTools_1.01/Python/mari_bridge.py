# ------------------------------------------------------------------------------
# Mari-Nuke communication scripts
# - Nuke's "Mari bridge": communication to and from Mari
# 
# coding: utf-8
# Copyright (c) 2011 The Foundry Visionmongers Ltd.  All Rights Reserved.
# ------------------------------------------------------------------------------

import mari_bridge_server
from mari_bridge_server import debugMsg, errorMsg, setDebug

import math
import nuke
import os
import pickle
import socket
import subprocess
import threading

_enable_socket = False
_actual_port = None
_default_listen_port = 50107
_default_send_port = 6100
_default_port_range = 200
_single_port_text = 'single port only'
_current_mari_pid = None
_current_mari_host = None
_current_mari_port = None
_response_timeout_sec = 3               # number of seconds to wait on a connection before deciding it isn't Mari
_response_timer = None                  # Timer thread object
_pending_commands = []                  # commands waiting for a response before sending
_have_valid_mari_path = None            # unchecked
_install_path_var = 'MARI_INSTALL_PATH'
_mari_path = os.environ[_install_path_var] if os.environ.has_key(_install_path_var) else ''
_script_loaded = False
_version_checked = False
_uv_tile_supported = True               # assume supported until checked (change this behaviour if needed)

#-------------------------------------------------------------------------------
def version():
    "Returns a string indicating the version of Mari that this Mari bridge script comes from."
    # Cache the result if required
    if not hasattr(version, '_cached'):
        def readVersion():
            data_file_name = os.path.split(__file__)[0] + '/nuke_mari.dat'
            try:
                text = open(data_file_name, 'rb').readlines()[0]
            except IOError:
                errorMsg("Couldn't find Nuke-Mari version info file: " + data_file_name)
                return
            try:
                return text.split('=')[1].strip()
            except IndexError:
                errorMsg("Invalid Nuke-Mari version info")
                return
        version._cached = readVersion()
    # Return the cached result
    return version._cached
    
#-------------------------------------------------------------------------------
class CancelledError(RuntimeError):
    "An exception to indicate a user cancellation."
    pass

#-------------------------------------------------------------------------------
class _NodeSizes:
    """Screen sizes in pixels of various nodes.
    
    We can't calculate the display sizes of the nodes until they've been placed and drawn correctly,
    so for now we'll just use predefined values as we know what they'll be.
    """
    READ_WIDTH = 80
    DOT_WIDTH = 12
    OTHER_WIDTH = 80
    READ_HEIGHT = 78
    DOT_HEIGHT = 12
    OTHER_HEIGHT = 20
    
    @classmethod
    def get(cls, node):
        "Call with a node to return a guess at the screen size of the node."
        node_class = node.Class()
        if node_class.startswith('Read'):
            return (cls.READ_WIDTH, cls.READ_HEIGHT)
        if node_class.startswith('Dot'):
            return (cls.DOT_WIDTH, cls.DOT_HEIGHT)
        return (cls.OTHER_WIDTH, cls.OTHER_HEIGHT)

#-------------------------------------------------------------------------------
# ToMari
#-------------------------------------------------------------------------------
class ToMari():
    def __init__( self, name=None, geo_list=None, data_dir=None, image=None, camera=None ):
        """Creates a data collection to describe a projection setup or parts of one.
        
        Later it sends the data to Mari via the socket connection to re-create it, or exports it to disk.
        """
        self.name = name
        if self.name is None:
            self.name = 'Nuke_' + os.path.splitext(os.path.basename(nuke.Root().name()))[0]
        self.geo_list = geo_list or []                                                      # list the paths to the objects
        self.data_dir = data_dir or getMariDataDir()                                        # store the path to the data dir used for temp files
        self.lut = None
        activeViewer = nuke.activeViewer()
        if activeViewer is not None:
            if activeViewer.node()['viewerProcess'].value() != 'None':
                self.lut = getLUT()

        self.projections = list( dict(image=dict( paths=dict(),     # path dictionary uses frame as key and path as value
                                                  width=0,
                                                  height=0,
                                                  pixel_aspect=1
                                                  ),
                                      camera=dict( name='',
                                                   data=list( dict( # describe the camera
                                                                    frame=0,
                                                                    fovx=0.0,
                                                                    fovy=0.0,
                                                                    ortho=False,              # ortho or perspective?
                                                                    haperture=0.0,            # for future reference
                                                                    vaperture=0.0,            # for future reference
                                                                    focal=0,                  # for future reference
                                                                    look_at_pos=(0.0,0.0,0.0),
                                                                    up_vect=(0.0,0.0,0.0)
                                                                    )
                                                              )
                                                   )
                                      )
                                 )
        
    #-------------------------------------------------------------------------------
    def dataSet( self ):
        return dict( name=self.name, geo_list=self.geo_list, data_dir=filenameFilter( self.data_dir ), lut=self.lut, proj_data=self.projections )

    #-------------------------------------------------------------------------------
    def exportToFile( self, name=None ):
        """Exports the data to a file, so it can be imported in Mari as an alterntive workflow to the socket connection.
        
        @param name:    The name of the exported file. If this is just the name, the script settings' "mari location dir" will
                        be used; if it's a valid file path, that will be used instead. If it's None, a file browser will pop up.
        """
        # Check the name, and append an extension if required
        if name is None:
            name = nuke.getFilename( 'Export Mari Projection', pattern='*.nmb', default=getMariDataDir()+'/',type='save' )

        ext = os.path.splitext( name )[1]
        if ext != '.nmb':
            name = name + '.nmb'

        # Get the output path
        if os.path.exists( os.path.dirname( name ) ):
            output_path = name
        else:
            output_path = getMariDataDir() + '/' + name

        # Write the data set to disk
        with open( output_path, 'w' ) as exportFile:
            debugMsg('writing data set to: ' + output_path)
            pickle.dump( self.dataSet(), exportFile )

    #-------------------------------------------------------------------------------
    def newProject( self ):
        """Creates a new project in Mari via the socket connection.
        
        TO DO: replace this with a method in Mari's ToNuke class.
        """
        data_dir = getMariDataDir()
        panel = nuke.Panel( 'Mari Channel Properties' )
        panel.addSingleLineInput( 'name', 'colour' )
        panel.addEnumerationPulldown('resolution', '256x256 512x512 1024x1024 2048x2048 4096x4096 8192x8192 16384x16384 32768x32768')
        if panel.show():
            width, height = [ int(r) for r in panel.value( 'resolution' ).split('x') ]
            name = panel.value( 'name' )
            new_chan = [ {'name': name, 'width': width, 'height':height, 'useAlpha':True} ]
            sendToMari( 'mari.system.nuke_bridge.startNewProject( "%s", %s, "%s", %s, %s )' % ( self.name, self.geo_list, data_dir, new_chan, self.lut ) )

    #-------------------------------------------------------------------------------
    def sendProjectorData( self ):
        "Creates a new projector in Mari via the socket connection."
        debugMsg('sending %s projections' % len(self.projections))
        sendToMari('mari.system.nuke_bridge.FromNuke(%s).createProjectors()' % self.dataSet(), allow_set_fg=True)

#-------------------------------------------------------------------------------
# ParseNodes
#-------------------------------------------------------------------------------
class ParseNodes():
    def __init__( self, nodes ):
        "Parses node selection and stores relevant nodes according to their type, for easy access by the helper methods."
        self.nodes = nodes
        self.geo_nodes = self.getGeoNodes()
        self.proj_nodes = self.getProjNodes()
        self.viewerProcess = 0
        
    #-------------------------------------------------------------------------------
    def getGeoNodes( self ):
        "Returns geo nodes only."
        debugMsg('collecting geo nodes')
        geo_nodes = [ n for n in self.nodes if set( ('display', 'render_mode') ).issubset( set( n.knobs() ) ) or n.Class()=='PoissonMesh']
        cards = [n for n in geo_nodes if n.Class().startswith( 'Card' ) and 'image_aspect' in n.knobs()]
        illegal_cards = [n for n in cards if n['image_aspect'].value()]
        if illegal_cards:
            if not nuke.ask('The following cards are set to use the incoming image aspect\nand will therefore be incompatible with returning UV textures:\n' + \
                        '\n'.join([n.name() for n in illegal_cards]) + '\n\nContinue anyway?'):
                raise CancelledError()
        return geo_nodes
    
    #-------------------------------------------------------------------------------
    def getProjNodes( self ):
        "Returns a list of dictionaries with camera and image node - one for each Project3D node in nodes."
        debugMsg('collecting projection nodes')
        proj_nodes = []
        for node in self.nodes:
            if node.Class() == 'Project3D':
                proj_nodes.append({'project': node, 'camera': findFirstActiveNode(node.input(1)), 'image': node.input(0)})
        return proj_nodes

#-------------------------------------------------------------------------------
# Socket communication functions
#-------------------------------------------------------------------------------
def getMariHostAndPort():
    """Returns the details of the current Mari host connection.
    
    @rtype:     (str, int)
    @return:    (host, port)
    """
    host = nuke.root()['hostName'].value().strip() or 'localhost'
    try:
        port = int(nuke.root()['socketPortSend'].value())
    except ValueError:
        global _default_send_port
        return (socket.gethostname(), _default_send_port)
    
    return (host, port)

#-------------------------------------------------------------------------------
def getNukeHostAndPort():
    """Returns the details of the current Nuke server connection.
    
    If the Mari host is set to localhost, the Nuke host will be the same.
    Otherwise, the Nuke host will be the current host name.
    @rtype:     (str, int)
    @return:    (host, port)
    """
    global _actual_port
    mari_host, mari_port = getMariHostAndPort()
    # If the Mari host is a variant of 'localhost', use it for consistency
    if hostNamesMatch(mari_host, 'localhost'):
        nuke_host = mari_host
    else:
        nuke_host = socket.gethostname()
    return nuke_host, _actual_port

#-------------------------------------------------------------------------------
def sendToMari(mari_cmd, force_host=None, force_port=None, ignore_failure=False, set_nuke_host=True, allow_set_fg=False):
    """Sends a command to Mari via a socket connection.
    
    The command port in Mari's preferences needs to be enabled for this to work.
    @type force_host:       str
    @param force_host:      Name of the host to send to, or None to use the current host
    @type force_port:       int
    @param force_port:      Port to connect to on the host, or None to use the current one
    @type mari_cmd:         str
    @param mari_cmd:        Mari Python command to run.  This may be blank to just verify the connection
    @type ignore_failure:   bool
    @param ignore_failure:  Set to True to ignore socket errors on transmission
    @type set_nuke_host:    bool
    @param set_nuke_host:   If True (the default), this prepends a command to set the current Nuke host
    @type allow_set_fg:     bool
    @param allow_set_fg:    Set to True to allow Mari to set the foreground window in response to this command
    @rtype:                 bool
    @return:                True if the command was sent successfully, or False otherwise
    """
    messageFn = debugMsg if ignore_failure else errorMsg
    
    # Check the connection details
    mari_host, mari_port = getMariHostAndPort()
    this_machine, this_port = getNukeHostAndPort()
    if this_port is None:
        nuke.root()['enableSocket'].setValue(True)
        this_machine, this_port = getNukeHostAndPort()
        if this_port is None:
            error_msg = "Nuke server is not running"
            messageFn(error_msg)
            if not ignore_failure:
                nuke.message("<p><b>" + error_msg + ".</b></p>" + \
                             "Nuke-Mari communication requires a connection from Mari to Nuke, and the Nuke server is not running. " + \
                             "Please check your configuration and try again.")
            return False
    
    # Override the Mari host and port if specified
    if force_host is not None:
        mari_host = force_host
    if force_port is not None:
        mari_port = force_port
    
    # Connect to Mari
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    debugMsg('Connecting to Mari on %s:%d' % (mari_host, mari_port))
    try:
        s.connect((mari_host, mari_port))
    except socket.error as err:
        messageFn("Socket error: '%s'" % str(err))
        if not ignore_failure:
            nuke.message("<b>Nuke can't connect to the Mari host on %s:%d.</b>" % (mari_host, mari_port) + \
                         "<p>Please check the following:</p>" + \
                         "<ul><li>Mari is running" + \
                         "<li>The Mari host in Nuke's \"Mari\" tab (script settings) is set to the correct IP address or host name" + \
                         " (leave blank if running Mari on the same machine)" + \
                         "<li>The Mari port number in Nuke's \"Mari\" tab matches the command port number in Mari's preferences" + \
                         "<li>The command port is enabled in Mari's preferences" + \
                         "<li>Both machines are connected to the same network (can you ping the Mari host?)" + \
                         "<li>If running Mari on a different machine, \"Local Host Only\" - in the Mari preferences, under" + \
                         " \"Scripts\" - must not be set</ul>")
        return False
    
    # Request verification if the command is empty or if this is the first connection
    global _current_mari_pid
    verify_connection = (mari_cmd == '' or _current_mari_pid is None)
    
    # Allow foreground window setting when appropriate
    if allow_set_fg:
        allowMariToSetFGWindow(mari_host)
    
    # Add Nuke host setting to the command when appropriate
    if mari_cmd != '':
        mari_cmd += '\x04'
    if set_nuke_host:
        mari_cmd = 'mari.system.nuke_bridge.setNukeHost("%s", %d, %d)\x04' % (this_machine, this_port, os.getpid()) + mari_cmd
    
    trace_cmd = mari_cmd[:100]
    if len(trace_cmd) < len(mari_cmd):
        trace_cmd += "..."
    debugMsg("Sending: '%s'" % trace_cmd)
    
    # Send the command
    try:
        s.send(mari_cmd)
    except socket.error as err:
        messageFn("Socket error: '%s'" % str(err))
        return False
    
    # When verifying connections, wait a set time and check if active
    if verify_connection:
        global _response_timer
        if _response_timer is None:
            debugMsg('Starting response timer')
            global _response_timeout_sec
            _response_timer = threading.Timer(_response_timeout_sec, responseTimerExpired)
            _response_timer.start()
    
    return True

#-------------------------------------------------------------------------------
def hostNamesMatch(host1, host2):
    "Returns True iff the given host names match, accounting for the various equivalent names of 'localhost' etc."
    def getAllNameAliases(host):
        def addNameAliases(host, target_set):
            "Adds the host name, IP, and fully-qualified domain name to the set."
            try:
                [target_set.add(var) for var in (host, socket.gethostbyname(host), socket.getfqdn(host))]
            except socket.gaierror:
                pass        # host name look up failed; ignore for the purposes of the check
        
        local_host_names = set()
        [addNameAliases(h, local_host_names) for h in ('localhost', socket.gethostname())]
                                                                                        
        aliases = set()
        addNameAliases(host, aliases)
        # If there's any overlap between the host and localhost sets, add the entire localhost set
        if not aliases.isdisjoint(local_host_names):
            aliases = aliases.union(local_host_names)
        return aliases
    
    if host1 is None or host2 is None:
        return host1 == host2
    
    return host2 in getAllNameAliases(host1)

#-------------------------------------------------------------------------------
def toggleConnection(node, knob):
    global _script_loaded
    
    port_enabled = knob.value()
    if not _script_loaded:
        # Delay any required socket enable until the script is loaded, as the knobs aren't all correctly attached yet
        global _enable_socket
        _enable_socket = port_enabled
        knob.setValue( False )
    else:
        setConnectionActive(port_enabled)
    
#-------------------------------------------------------------------------------
def setConnectionActive(active):
    global _actual_port
    
    node = nuke.root()
    knob = node['enableSocket']
    
    # Check for a valid port number
    port_knob = node['socketPort']
    port_knob.setEnabled(not active)
    try:
        port = int(port_knob.value())
    except ValueError:
        global _default_listen_port
        port = _default_listen_port
        port_knob.setValue(port)
    
    localhost_knob = node['localhostOnly']
    localhost_knob.setEnabled(not active)
    
    # Set up to check one port or a number of ports in a range
    if node['enablePortRange'].value() == _single_port_text:
        max_port_to_check = port
    else:
        max_port_to_check = port + max(node['portRange'].value() - 1, 0)
    
    # Try to start or stop the server
    status = ''
    port_status_knob = node['cmdStatus']
    mari_host, mari_port = getMariHostAndPort()
    same_host = hostNamesMatch('localhost', node['hostName'].value())
    if active:
        test_port = port
        while True:
            if not (same_host and test_port == mari_port):
                try:
                    mari_bridge_server.serve(test_port, localhost_only=localhost_knob.value())
                    _actual_port = test_port
                    status = 'Listening on port ' + str(test_port)
                    break
                except ValueError:
                    pass            # try the next port
                except Exception as err:
                    status = 'Error: ' + str(err)
                    break
            # Couldn't start the server on the given port
            test_port += 1
            if test_port > max_port_to_check:
                # We can't toggle the enable knob off again during a callback, so just change the status and show a message
                if max_port_to_check == port:
                    port_in_use_msg = "Port %d is already in use" % port
                else:
                    port_in_use_msg = "Ports %d-%d are already in use" % (port, max_port_to_check)
                status = 'Error: ' + port_in_use_msg
                msg =   "<b>" + port_in_use_msg + ".</b><p>" + \
                        "Either close the application that uses it (if it's another Nuke session, just deactivate the " + \
                        "command port in the project settings) or use a different port number."
                nuke.executeInMainThread(lambda: nuke.message(msg))
                break
    else:
        if _actual_port is not None:
            disconnectFromMari()
            mari_bridge_server.stopConnection(_actual_port)
            _actual_port = None
        status = "Disabled"
    
    port_status_knob.setValue('<b>' + status + '</b>')

#-------------------------------------------------------------------------------
def updateSendStatus():
    "Updates the 'send status' knob in the Mari tab."
    root = nuke.root()
    # Check that we have all the knobs we need
    try:
        if any((root.knob(name) is None for name in ('hostName', 'socketPortSend', 'sendStatus'))):
            return          # not all knobs have been created yet
    except ValueError:  # not attached to a node
        return
    
    global _current_mari_pid
    if _current_mari_pid is not None:
        status = "Talking to Mari on " + str(root['hostName'].value()) + ':' + str(root['socketPortSend'].value())
    else:
        status = "Inactive"
    root['sendStatus'].setValue('<b>' + status + '</b>')

#-------------------------------------------------------------------------------
def setCurrentNukeFor(pid, is_current, mari_version=''):
    """Indicates that this is, or no longer is, the Nuke for communicating with the Mari with the given process ID.
    
    @type mari_version:     str
    @param mari_version:    The string version of Mari; '' for pre-1.4v3, or None to not check now
    """
    # Cancel any currently active connection check, providing this is setting the connection as active
    global _response_timer
    if is_current and _response_timer is not None:
        debugMsg('Received response from Mari')
        processResponse(mari_version)
    
    # Check whether this is from the current Mari
    global _current_mari_pid
    global _current_mari_host
    global _current_mari_port
    if pid == _current_mari_pid:
        # Received from the current Mari
        if not is_current:
            _current_mari_pid = None
            _current_mari_host = None
            _current_mari_port = None
    else:
        # Received from a new Mari
        _current_mari_pid = pid
        _current_mari_host, _current_mari_port = getMariHostAndPort()
        
    updateSendStatus()

#-------------------------------------------------------------------------------
def setMariHost(name, port, pid):
    """Sets the host name, port, and process ID of the Mari instance that Nuke should connect to.
    
    This function is only intended to be called from Mari via a socket.
    """
    root = nuke.root()
    host_knob = root['hostName']
    if not hostNamesMatch(host_knob.value(), name):     # don't override the current name if it's just an alias
        host_knob.setValue(name)
    root["socketPortSend"].setValue(port)
    setCurrentNukeFor(pid, True, None)                  # don't check versions now
    # Acknowledge the communication from Mari
    nuke_script_version = version()
    if nuke_script_version is not None:
        nuke_script_version = "'%s'" % nuke_script_version
    sendToMari("mari.system.nuke_bridge.setCurrentMariFor(%d, True, %s)" % (os.getpid(), nuke_script_version), set_nuke_host=False)

#-------------------------------------------------------------------------------
def disconnectFromMari():
    "Tells any connected Mari instance that we're disconnecting."
    global _current_mari_pid
    if _current_mari_pid is not None:
        global _current_mari_host
        global _current_mari_port
        sendToMari('mari.system.nuke_bridge.setNukeHost(None, None, %d)' % os.getpid(), force_host=_current_mari_host,
                   force_port=_current_mari_port, ignore_failure=True, set_nuke_host=False)
        _current_mari_pid = None
        updateSendStatus()

#-------------------------------------------------------------------------------
def closeAllConnections():
    "Closes any incoming and outgoing connections related to the Nuke-Mari bridge."
    debugMsg('Closing all connections')
    disconnectFromMari()
    root = nuke.root()
    try:
        socket_knob = root.knob('enableSocket')
    except ValueError:          # not attached to a node
        socket_knob = None
    if socket_knob is not None and socket_knob.value():
        socket_knob.setValue(False)     # the callback will turn off the connection

#-------------------------------------------------------------------------------
def processResponse(mari_version):
    """Processes a response to a setCurrentNukeFor command.
    
    @type mari_version:     str
    @param mari_version:    The string version of Mari; '' for pre-1.4v3, or None to not check now
    """
    global _response_timer
    assert(_response_timer is not None)
    _response_timer.cancel()
    _response_timer = None
    
    global _version_checked
    if not _version_checked and mari_version is not None:
        _version_checked = True
        # Warn if the script version of the Nuke side is lower than the Mari side (higher is fine)
        nuke_version = version()
        if nuke_version is not None:    # don't check if we have no version - the settings file is missing for some reason
            nuke_version_num = getNumericVersion(nuke_version)
            mari_version_num = getNumericVersion(mari_version)
            debugMsg("Checking versions: Nuke side is %s (%d), Mari side is %s (%d)" \
                     % (nuke_version, nuke_version_num, mari_version, mari_version_num))
            if nuke_version_num < mari_version_num:
                if mari_version is None:
                    mari_version = "(1.4v2 or earlier)" # should never be used, as this should never be greater than the Nuke script version
                nuke.message("<b>Nuke is using an old version of the Nuke&lt;&gt;Mari bridge code.</b><p>" \
                             + "The Nuke&lt;&gt;Mari bridge code being used by Nuke is from Mari version <b>%s</b>, " % nuke_version \
                             + "which is older than the currently-running version of Mari: <b>%s</b>.  " % mari_version \
                             + "This may result in problems, or missing functionality.<p>" \
                             + "We recommend that you install the latest version, as described in the Nuke&lt;&gt;Mari bridge " \
                             + "help document, before continuing.")
    
    # Execute pending commands
    global _pending_commands
    commands = _pending_commands
    _pending_commands = []              # reset in case a callback function appends a new command
    for cmd in commands:
        exec cmd

#-------------------------------------------------------------------------------
def getNumericVersion(version_str):
    """Returns an integer representation of the given version string.
    
    The integers generated in this way will match mari.AppVersion.number() in scale.
    """
    if version_str is None:
        return 0
    version_str = version_str.lower()
    try:
        maj_str, rest = version_str.split('.')
        majmin = 10000000 * int(maj_str)
        if rest.endswith('dev'):
            min_str, rest = rest.split('dev')
        else:
            min_str, rest = rest.split('v')
        majmin += 100000 * int(min_str)
        
        if rest == '':
            return majmin + 99999                                       # dev = max version
        if rest.find('a') >= 0:
            rev_str, rest = rest.split('a')
            return majmin + 1000 * int(rev_str) + 1 * 100 + int(rest)   # stage = 1
        if rest.find('b') >= 0:
            rev_str, rest = rest.split('b')
            return majmin + 1000 * int(rev_str) + 2 * 100 + int(rest)   # stage = 2
        
        return majmin + 1000 * int(rest) + 3 * 100                      # stage = 3
        
    except (IndexError, ValueError):
        return 0

#-------------------------------------------------------------------------------
def responseTimerExpired():
    "Timer function to call when that a Mari connection has failed."
    global _response_timer
    _response_timer = None
    
    # Cancel pending commands
    global _pending_commands
    _pending_commands = []
    
    msg = "Nuke could not communicate with Mari"
    errorMsg(msg)
    nuke.executeInMainThread(nuke.message,
                             "<p><b>" + msg + ".</b></p>" + \
                             "<p>The socket connection succeeded, but did not get a response from Mari.  This could mean:<ul>" + \
                             "<li>Your version of Mari is earlier than 1.3v2 and does not contain the Nuke-Mari workflow functionality" + \
                             "<li>A different application is using port <b>%s:%d</b>" % getMariHostAndPort() + \
                             "<li>Mari is currently unresponsive due to a long-running operation"
                             "</ul></p><p>Please check the configuration and try again.</p>")

#-------------------------------------------------------------------------------
def checkAndCall(function_call_text):
    """Checks that the Nuke-Mari connection is active, and then calls the given function.
    
    @type  function_call_text: str
    @param function_call_text: The text of the function to call after checking
    """
    global _pending_commands
    # Send an empty command to verify the connection.  The function will fail if the command couldn't be sent at all.
    # If it succeeds, we add a pending command, which will be executed if and when a response was received.
    if sendToMari(''):      # verify connection
        _pending_commands.append(function_call_text)

#-------------------------------------------------------------------------------
# Other functions
#-------------------------------------------------------------------------------
def allowMariToSetFGWindow(host_name):
    # We only need this on Windows.  On Linux, anything can set the foreground window anyway.
    # There's also no need to do this if Mari isn't running on the same machine
    if not nuke.env['WIN32'] or host_name not in ('localhost', socket.gethostname()):
        return
    
    # Use CTypes to call the Windows API function to allow an app to set the foreground window
    import ctypes
    user32 = ctypes.windll.LoadLibrary('user32.dll')
    # Allow just Mari to set the FG window, if we have its PID; otherwise, allow anything
    allow_pid = _current_mari_pid if _current_mari_pid is not None else -1
    user32.AllowSetForegroundWindow(allow_pid)

#-------------------------------------------------------------------------------
def _copyKnobsFromScriptToScript(source, target):
    k1 = source.knobs()
    k2 = target.knobs()
    excluded_knobs = ["name", "xpos", "ypos"]
    intersection = dict([(item, k1[item]) for item in k1.keys() if item not in excluded_knobs and k2.has_key(item)])
    [target[k].fromScript(source[k].toScript(False)) for k in intersection.keys()]

#-------------------------------------------------------------------------------
def _bakeCam( node, frame_range ):
    "Bakes an animated camera in preparation for fbx export."
    cam = nuke.nodes.Camera2( useMatrix=True )
    cam['matrix'].setAnimated()
    cam['label'].setValue( node.name() + ' baked' )
    
    for frame in frame_range:
        for idx in xrange(16):
            matrix = node['world_matrix'].valueAt( frame )[idx]
            cam['matrix'].setValue( matrix, idx, frame )
            debugMsg(matrix)
    return cam

#-------------------------------------------------------------------------------
def browseForMariPath():
    "Browses for the Mari executable."
    global _mari_path
    mari_location = _mari_path
    while True:
        mari_location = nuke.getFilename('Select Mari executable', default=mari_location)
        if mari_location is None:
            return None
        if os.path.isfile(mari_location):
            break
        mari.utils.message('Please select an executable file to run.')
    _mari_path = mari_location
    nuke.root().knob('mariLocation').setValue(_mari_path)
    checkMariLocation()
    return _mari_path

#-------------------------------------------------------------------------------
def checkMariLocation():
    "Checks the validity of the Mari executable location specified in the knob."
    global _mari_path
    global _have_valid_mari_path
    global _install_path_var
    try:
        _mari_path = nuke.root().knob('mariLocation').value()
    except ValueError:      # not attached to a node
        _have_valid_mari_path = None
        return
    _have_valid_mari_path = os.path.isfile(_mari_path)
    if _have_valid_mari_path:
        os.environ[_install_path_var] = _mari_path

#-------------------------------------------------------------------------------
def launchMari():
    global _mari_path
    global _have_valid_mari_path
    mari_location = _mari_path
    
    # If we haven't done so, check if the path is valid
    if _have_valid_mari_path is None:
        _have_valid_mari_path = os.path.isfile(_mari_path)
    # Ask the user if we don't have a valid location
    if not _have_valid_mari_path:
        mari_location = browseForMariPath()
        if mari_location is None:
            return
    
    mari_args = [mari_location]
    mari_dir, mari_file = os.path.split(mari_location)
    if mari_file == 'MriBin':
        mari_dir = os.path.split(mari_dir)[0]   # effectively go up one directory
    launch_file = mari_dir + '/Media/Scripts/mari/system/enable_server_connection.py'
    if os.path.isfile(launch_file):
        mari_args.append(launch_file)
    
    # Launch Mari
    try:
        subprocess.Popen(mari_args)
    except Exception as err:
        nuke.message("Error launching '%s':<p>%s" % (mari_location, str(err)))
        _have_valid_mari_path = False
        return
    
    # Get ready to receive data from Mari
    nuke.root()['enableSocket'].setValue( True )

#-------------------------------------------------------------------------------
def showError(msg):
    """Shows an error message to the user in an appropriate form.
    
    In interactive mode, this shows a message box; otherwise, it reaises a ValueError.
    """
    if not nuke.INTERACTIVE:
        raise ValueError(msg)
    nuke.message(msg)

#-------------------------------------------------------------------------------
def exportProjectors( use_socket=False, sequence=False):
    """Exports projection setups in the currently selected nodes.
    
    This either sends them via the socket, or exports them to a file.
    """
    # Get the geo nodes
    try:
        pn = ParseNodes(nuke.selectedNodes())
    except CancelledError:
        return
    geo_nodes = pn.geo_nodes
    proj_nodes = pn.proj_nodes

    tm = ToMari()
    tm.projections = []
    if sequence:
        # Ask the user for a frame range
        first = nuke.root().firstFrame()
        last = nuke.root().lastFrame()
        user_input = nuke.getInput( 'Export Projections for frames:', '%s-%sx%s' % ( first, last, int(float(last-first+1)/3) ) )
        if not user_input:
            return
        if ',' in user_input:
            # Assume that a list of frames was requested
            frame_range = [ int(f.strip()) for f in user_input.split(',') ]
        else:
            # Assume that a range with upper and lower bounds was requested
            frame_range = nuke.FrameRange( user_input )
    else:
        # Current frame
        frame_range = [nuke.frame()]

    # Check for correct supplied nodes
    if not proj_nodes:
        return showError('At least one Project3D node needs to be included in the node selection if sending into an open Mari project.\n\n' + \
                         'To start a new Mari project, select at least one geometry node as well.')
    
    # Check for images on Project3D inputs
    missing_images = [info for info in proj_nodes if info['image'] is None]
    if missing_images != []:
        return showError("The following Project3D nodes need to have images connected to their inputs to send projection data to Mari:\n\n" + \
                         ", ".join([info['project'].name() for info in missing_images]))
        
    # Check that all Project3D nodes have attached cameras
    missing_cameras = [info for info in proj_nodes if info['camera'] is None]
    if missing_cameras != []:
        return showError("The following Project3D nodes need to have attached Camera nodes before sending to Mari:\n\n" + \
                         ", ".join([info['project'].name() for info in missing_cameras]))
    
    # Geometry nodes
    if geo_nodes:
        for gn in geo_nodes:
            tm.geo_list.append( getGeo( gn ) )

    # Export
    try:
        for pn in proj_nodes:
            debugMsg('exporting ' + pn['camera'].name())
            img_node = pn['image']
            cam_node = pn['camera']
            camera_data = getCamData( cam_node, frame_range )
            image_data = dict(paths=getImg( img_node, frame_range ), width=img_node.width(), height=img_node.height(),
                              pixel_aspect=img_node.pixelAspect())
            proj_set = dict( image=image_data, camera=camera_data )
            tm.projections.append( proj_set )
    except CancelledError:
        return
    except Exception as err:
        if not isinstance(err, RuntimeError) or str(err) != "Cancelled":            # Don't show an error for the user cancelling
            errorMsg("Error exporting projection data: " + str(err))
            nuke.message("<b>Error exporting projection data from Nuke.</b><p>" + str(err))
        return

    # Send via the socket, or export to disk
    if use_socket:
        tm.sendProjectorData()
    else:
        tm.exportToFile()

#-------------------------------------------------------------------------------
def focalToFov ( focal, aperture ):
    "Converts focal length and aperture to FOV."
    return math.degrees(math.atan2(aperture / 2, focal) * 2)

#-------------------------------------------------------------------------------
def getMariDataDir():
    """Returns the Mari data directory.
    
    This checks if the custom knob "mariDataDir" exists in script settings and use it's value to point to the "mariData" dir.
    If it doesn't exist or is empty, a "mariData" dir will be created in nuke's cache path and the respective path will be returned.
    """
    default_path = nuke.value('preferences.DiskCachePath') + '/mariData'

    # Try to get the value from the root knob
    try:
        custom_dir = nuke.value( 'root.mariDataDir' )
    except:
        custom_dir = None

    # Use a default if the root knob is empty
    if not custom_dir:
        custom_dir = default_path
    if not os.path.isdir( custom_dir ):
        os.makedirs( custom_dir )
    
    # take the absolute path to avoid any ambiguity
    custom_dir = os.path.abspath(custom_dir)

    # Paths sometimes come back as "C://something", which doesn't work reliably because of the double slash.
    # Check for that and fix it (but only the specific case to ensure UNC paths still work)
    custom_dir = custom_dir.replace("://", ":/")
    # convert Windows back slashes to forward
    custom_dir = custom_dir.replace("\\", "/")
    
    return custom_dir

#-------------------------------------------------------------------------------
def getWorldMatrix( node, frame ):
    "Gets a 3D node's world matrix."
    debugMsg('getting matrix for %s at frame %s' % ( node.name(), frame ))
    mknob = node['world_matrix']
    mtx = nuke.math.Matrix4()
    #for index in range(0, 16):
        #mtx[index] = node['world_matrix'].value(index % 4, index / 4)  
    for index in xrange(mknob.arraySize()):
        mtx[index] = mknob.valueAt(frame)[index]
    mtx.transpose()
    return mtx

#-------------------------------------------------------------------------------
def getCamData( cam_node, frame_range ):
    """Converts Nuke camera data into Mari camera data at a given frame (Euler to Vector, filmback and focal to fov, etc).
    
    @param cam_node:    Nuke Camera node
    @param frame_range: Frames to get values at
    @return:            A dictionary with name and data keys, where data holds a dictionary for each key frame with frame, position,
                        look-at position, up vector, hfov, vfov, focal, haperture and vaperture
    """
    cam_data = []
    for frame in frame_range:
        cam_frame_data = { 'frame':frame }
        # Collect the data that we don't have to convert
        for k in ( 'haperture', 'vaperture', 'focal' ):
            cam_frame_data[ k ] = cam_node[k].valueAt( frame )
        cam_frame_data[ 'ortho' ] = cam_node['projection_mode'].value() == 'orthographic'

        # Field of view
        cam_frame_data['hfov'] = focalToFov( cam_node['focal'].valueAt( frame ), cam_node['haperture'].valueAt( frame ) )
        cam_frame_data['vfov'] = focalToFov( cam_node['focal'].valueAt( frame ), cam_node['vaperture'].valueAt( frame ) )

        # Get transforms
        cam_matrix = getWorldMatrix( cam_node, frame )

        # Position
        cam_vect = cam_matrix.transform( nuke.math.Vector3(0,0,0) )
        cam_frame_data['cam_pos'] = ( cam_vect.x, cam_vect.y, cam_vect.z )

        # Up vector
        upVect = cam_matrix.yAxis()
        cam_frame_data['up_vect'] = ( upVect.x, upVect.y, upVect.z )

        # Look-at position
        world_look_at_vect = nuke.math.Vector3(0,0,-1)
        look_at_vect = cam_matrix.vtransform( world_look_at_vect )
        look_at = cam_vect + look_at_vect          
        cam_frame_data['look_at'] = ( look_at.x, look_at.y, look_at.z )        
        cam_data.append( cam_frame_data )
    
    return dict( name=cam_node.name(), data=cam_data )

#-------------------------------------------------------------------------------
def getGeo( geo_node ):
    """Returns the path to the obj for this geo, exporting if necessary.
    
    If geo_node has a file path pointing to an obj and no transforms, it just returns that path. Otherwise,
    it exports an obj and return the new path.
    If required, files will be exported to the mariData dir as set in the script settings.
    """
    identity_matrix = nuke.math.Matrix4()
    identity_matrix.makeIdentity()
    if 'file' in geo_node.knobs() and os.path.splitext( nuke.filename( geo_node ) )[1]=='.obj' and geo_node['transform'].value() == identity_matrix:
        return nuke.filename( geo_node )

    output_path = getMariDataDir()
    geo_path = output_path + '/%s.obj' % geo_node.name()
    gw_node = nuke.nodes.WriteGeo( file = geo_path, name='TEMP_NODE', tile_color=4278255615 )
    activeViewer = nuke.activeViewer()
    if activeViewer is not None:
        gw_node['views'].setValue( activeViewer.view() )
    gw_node.setInput( 0, geo_node )
    nuke.execute( gw_node, nuke.frame(), nuke.frame() )
    nuke.delete( gw_node )
    return filenameFilter( geo_path )

#-------------------------------------------------------------------------------
def getImageTempFileName(node, output_path, current_frame):
    "Returns a generated temporary image file name based on stats of the node and current frame."
    img_path = output_path + '/' + node.name() + '_'
    generated = False
    if node.knob('file') is not None:
        orig_file = node['file'].evaluate(time=current_frame)
        if orig_file is not None and orig_file != '':
            img_path += os.path.splitext(os.path.split(str(orig_file))[1])[0]       # file name without path or ext
            generated = True
    if not generated:
        img_path += '%06d' % current_frame
    return img_path + '.exr'
    
#-------------------------------------------------------------------------------
def checkMultiOverwrite(file_names):
    """Asks the user if they want to overwrite an individual file, and supplies a "yes/no to all" box.
    
    If one or fewer file names is supplied, the dialog is skipped entirely.  Callers of this function
    will still need to check for files that are not in this set in case the underlying file system
    changes while the dialog is visible.
    @rtype:  (set(str), set(str))
    @return: A set of the file names to overwrite, and a set of those to leave
    @raise:  CancelledError if the user cancelled the operation
    """
    import nukescripts
    class OverwritePanel(nukescripts.PythonPanel):
        def __init__(self, file_names):
            super(OverwritePanel, self).__init__()
            self.text = nuke.Text_Knob('name', '', 'Overwrite files?')
            self.all = nuke.Boolean_Knob('all', 'check/uncheck all', True)
            self.all.setFlag(nuke.ENDLINE)
            self.div = nuke.Text_Knob('divider', '')
            self.file_knobs = []
            for fname in file_names:
                name = os.path.split(fname)[1]
                fknob = nuke.Boolean_Knob(fname, name, True)
                fknob.setFlag(nuke.ENDLINE)
                self.file_knobs.append(fknob)
            knobs = [self.text, self.all, self.div]
            knobs.extend(self.file_knobs)
            [self.addKnob(k) for k in knobs]
        def knobChanged(self, knob):
            if knob.name() == 'all':
                val = knob.value()
                [fknob.setValue(val) for fknob in self.file_knobs]
    
    # Don't do anything if there are one or fewer files
    if len(file_names) < 2:
        return set(), set()
    
    panel = OverwritePanel(file_names)
    if not panel.showModalDialog():
        raise CancelledError("Overwrite cancelled")
    overwrites = set()
    leaves = set()
    for fknob in panel.file_knobs:
        if fknob.value():
            overwrites.add(fknob.name())
        else:
            leaves.add(fknob.name())
    return overwrites, leaves

#-------------------------------------------------------------------------------
def getImg( node, frame_range ):
    """Returns image paths from a node for a given frame range.
   
    If nuke.filename returns empty for node, an exr is rendered to output_path and its new path is returned.
    Also, if node's bbox is not compatible with Mari, a re-formatted version will be rendered.
    If nuke.filename is valid and already compatible with Mari, the file path is returned as is.
    
    @param node:        2D Nuke node
    @param frame_range: Nuke FrameRange object or iterable list of integer frame numbers
    @return:            A dictionary with frames as keys and the respective file paths as values.
    """
    debugMsg('checking image node')
    all_paths = {}
    unsup_formats = ('.cin', '.dpx')     # list of unsupported image extensions to always prerender to EXR

    orig_frame = nuke.frame()
    output_path = getMariDataDir()
    files_to_overwrite = [getImageTempFileName(node, output_path, f) for f in frame_range]
    files_to_overwrite = [fname for fname in files_to_overwrite if os.path.isfile(fname)]
    overwrite_set, leave_set = checkMultiOverwrite(files_to_overwrite)      # may raise CancelledError
    
    for f in frame_range:
        nuke.frame( f )
        img_path = nuke.filename( node, nuke.REPLACE )

        if img_path:
            pass # Force EXR render for now to ensure colour spaces are correct
            #ext = os.path.splitext( img_path )[1]
            #if ext != '.exr' and ext not in unsup_formats:
                #all_paths[f] = img_path
                #continue
        
        img_path = getImageTempFileName(node, output_path, f)
        if os.path.isfile( img_path ):
            # Ask if we should re-render (if the user hasn't already selected from a dialog)
            if img_path in overwrite_set:
                overwrite = True
            elif img_path in leave_set:
                overwrite = False
            else:
                overwrite = nuke.ask('File already exists:\n' + img_path + '\n\nOverwrite?')
            # If we don't need to re-render, use the path as-is
            if not overwrite:
                all_paths[f] = filenameFilter( img_path )
                continue

        crop_node = nuke.nodes.Crop( name='RESET_DATA_WINDOW', tile_color=4278255615, crop=True )
        try:
            crop_node.setInput( 0, node )
            write_node = nuke.nodes.Write( file=img_path, proxy=img_path, file_type='exr', colorspace='linear', channels='rgba', name='TEMP_NODE', tile_color=4278255615 )
            try:
                activeViewer = nuke.activeViewer()
                if activeViewer is not None:
                    write_node['views'].setValue( activeViewer.view() )
                write_node.setInput( 0, crop_node )
                nuke.execute( write_node, nuke.frame(), nuke.frame() )
                all_paths[f] = filenameFilter( img_path )
            finally:
                nuke.delete(write_node)
        finally:
            nuke.delete(crop_node)
    
    nuke.frame( orig_frame )
    return all_paths

#-------------------------------------------------------------------------------
def createRead(img, scale=None, inpanel=True, uv_tile=None, mergemat_from=None, create_dot=False, create_multitexture=False):
    """Creates a read node for the texture coming back from Mari.
    
    @param uv_tile:             (tile_u, tile_v) or None to not use a UVTile2 node
    @param mergemat_from:       A node to combine the new node's output with using a MergeMat, or None
    @param create_dot:          True to create a Dot node after the others, or False to not create one
    @param create_multitexture: True to create a MultiTexture node after the others, or False to not do so
    @return:                    A list of the nodes created.  The first will always be a read node,
                                and all nodes will be in order of connection.
    """
    read_node = nuke.createNode('Read', 'file "%s"' % img, inpanel=inpanel)
    read_node.autoplace()
    spacing = 20
    xpos = read_node.xpos()
    ypos = read_node.ypos() + _NodeSizes.READ_HEIGHT + spacing
    nodes = [read_node]
    
    if scale is not None:
        reformat_node = nuke.nodes.Reformat(type='scale', resize='distort', xpos=xpos, ypos=ypos)
        reformat_node['scale'].setValue(scale)
        reformat_node.setInput(0, read_node)
        ypos += _NodeSizes.OTHER_HEIGHT + spacing
        nodes.append(reformat_node)
    
    if uv_tile is not None:
        # If UVTile2 is not supported, we don't need any of the rest of the nodes, so we can exit now
        global _uv_tile_supported
        if not _uv_tile_supported:
            return nodes
        # Set up the correct UV tile information, and connect the node to the most recently created
        # one from above
        try:
            uv_tile_node = nuke.nodes.UVTile2(tile_u=uv_tile[0], tile_v=uv_tile[1], xpos=xpos, ypos=ypos)
        except RuntimeError:
            # UVTile2 is not supported
            _uv_tile_supported = False
            return nodes
        uv_tile_node.setInput(0, nodes[-1])
        ypos += _NodeSizes.OTHER_HEIGHT + spacing
        nodes.append(uv_tile_node)
    
    if mergemat_from is not None:
        # Create a MergeMat node, and connect it to the most recently created node from above,
        # as well as the indicated node
        mergemat_node = nuke.nodes.MergeMat(xpos=xpos, ypos=ypos)
        mergemat_node.setInput(0, nodes[-1])
        mergemat_node.setInput(1, mergemat_from)
        ypos += _NodeSizes.OTHER_HEIGHT + spacing
        nodes.append(mergemat_node)
    
    if create_dot:
        dot_node = nuke.nodes.Dot(xpos=xpos + (_NodeSizes.READ_WIDTH - _NodeSizes.DOT_WIDTH + 1) / 2,
                                  ypos=ypos + (_NodeSizes.OTHER_HEIGHT - _NodeSizes.DOT_HEIGHT) / 2)
        dot_node.setInput(0, nodes[-1])
        ypos += _NodeSizes.OTHER_HEIGHT + spacing
        nodes.append(dot_node)
        
    if create_multitexture:
        multitexture_node = nuke.nodes.MultiTexture(xpos=xpos, ypos=ypos)
        multitexture_node.setInput(0, nodes[-1])
        ypos += _NodeSizes.OTHER_HEIGHT + spacing
        nodes.append(multitexture_node)
    
    return nodes

#-------------------------------------------------------------------------------
def createChannelNodes(chan_name, uv_file_names):
    """Sets up Read, UVTile2 and MergeMat nodes to read the channel textures from the given list.
    
    @type   chan_name:      str
    @param  chan_name:      Display name of the channel - may contain other components such as the mesh name
    @type   uv_file_names:  list of (int, str)
    @param  uv_file_names:  UVs and names of the texture files to create nodes for, in UDIM order
    """
    if type(uv_file_names) is not list or uv_file_names == []:
        raise TypeError("uv_file_names must be a non-empty list")
    if len(uv_file_names) == 1:
        createRead(uv_file_names[0][1])
        return
    
    group = nuke.nodes.Group(name=chan_name)
    with group:
        extents = []
        prev_node = None
        last_file_index = len(uv_file_names) - 1
        for index, (uv, file_name) in enumerate(uv_file_names):
            # Create a Read node and connect up its various helpers
            create_dot = prev_node is None
            create_multitexture = index == last_file_index
            new_nodes = createRead(file_name, uv_tile=(uv % 10, uv / 10), inpanel=False, mergemat_from=prev_node,
                                   create_dot=create_dot, create_multitexture=create_multitexture)
            [addNodeToExtents(n, extents) for n in new_nodes]
            prev_node = new_nodes[-1]
        # Backdrop
        createBGNodeFromExtents(chan_name, extents)
        # Output
        output = nuke.nodes.Output(xpos=prev_node.xpos(), ypos=prev_node.ypos() + prev_node.screenHeight() + 100)
        output.setInput(0, prev_node)
        
        # Add a support warning if needed
        global _uv_tile_supported
        if not _uv_tile_supported:
            sticky = nuke.nodes.StickyNote(label="Please update to the latest Nuke version for UVTile support.")
            if extents != []:
                sticky_width = 342      # calculating this doesn't work until it's been drawn
                sticky.setXYpos((extents[0] + extents[2] - sticky_width) / 2, extents[3] + 50)
    
    nuke.showDag(group)

#-------------------------------------------------------------------------------
def addNodeToExtents(node, extents):
    "Updates the stored extents to include the screen area of the specified node."
    left_x = node.xpos()
    top_y = node.ypos()
    right_x, bottom_y = _NodeSizes.get(node)
    right_x += left_x
    bottom_y += top_y
    
    if extents == []:
        extents.extend([left_x, top_y, right_x, bottom_y])
    else:
        extents[0] = min(extents[0], left_x)
        extents[1] = min(extents[1], top_y)
        extents[2] = max(extents[2], right_x)
        extents[3] = max(extents[3], bottom_y)

#-------------------------------------------------------------------------------
def createBGNodeFromExtents(name, extents):
    "Creates a background node from the stored node extents (if any), and resets the extents."
    if extents == []:
        return
    
    margin = 20
    extents = [extents[0] - margin, extents[1] - margin, extents[2] + margin, extents[3] + margin]
    nuke.nodes.BackdropNode(name=name, xpos=extents[0], ypos=extents[1],
                            bdwidth=extents[2] - extents[0], bdheight=extents[3] - extents[1])

#-------------------------------------------------------------------------------
def getLUT():
    "Builds a dictionary of viewer parameters which Mari can use to reconstruct the color-space with."
    lut = {}

    viewer = nuke.activeViewer()
    if viewer is not None:
        viewer_node = viewer.node()

        knob = viewer_node.knob('center_fstop')
        if knob is not None:
            lut['center_fstop'] = knob.value()

        knob = viewer_node.knob('gain')
        if knob is not None:
            lut['gain'] = knob.value()

        knob = viewer_node.knob('gamma')
        if knob is not None:
            lut['gamma'] = knob.value()

        knob = viewer_node.knob('viewerProcess')
        if knob is not None:
            # We only need to send the name of all standard viewer processes as Mari knows how to handle these itself.
            # All custom viewer processes must be saved out to a LUT file and the file name sent across.
            view = knob.value()
            if view in ('None', 'sRGB', 'rec709'):
                lut['view'] = knob.value()
            else:
                viewer_process_node = nuke.ViewerProcess.node()
                if viewer_process_node is not None:
                    viewer_process_node_copy = eval('nuke.nodes.%s()' % viewer_process_node.Class())
                    _copyKnobsFromScriptToScript(viewer_process_node, viewer_process_node_copy)

                    cms_node = nuke.nodes.CMSTestPattern()
                    viewer_process_node_copy.setInput(0, cms_node)

                    lut_node = nuke.nodes.GenerateLUT()
                    lut_file = getMariDataDir() + '/Nuke_' + view + '.3dl'
                    lut_node.knob('file').setValue(lut_file)
                    lut_node.setInput(0, viewer_process_node_copy)

                    lut_node.knob('generate').execute()

                    [nuke.delete(node) for node in (viewer_process_node_copy, cms_node, lut_node)]

                    lut['file'] = lut_file

    return lut

#-------------------------------------------------------------------------------
def sendLUT(enable_error=True):
    if nuke.activeViewer() is not None:
        sendToMari( 'mari.system.nuke_bridge.setLUT( %s )' % getLUT() )
    elif enable_error:
        msg = 'Unable to send LUT as there is no active viewer.'
        errorMsg(msg)
        nuke.message(msg)

#-------------------------------------------------------------------------------
def sendNodes(node_list, no_nodes_error_msg):
    "Sends images from the given nodes to Mari's Image Manager."
    img_list = []
    try:
        for node in node_list:
            img_list.append( getImg( node, [nuke.frame()] ).values()[0] )
    except CancelledError:
        return
    except Exception as err:
        if not isinstance(err, RuntimeError) or str(err) != "Cancelled":            # Don't show an error for the user cancelling
            errorMsg("Error sending images from nodes: " + str(err))
            nuke.message("<b>Error sending images from Nuke.</b><p>" + str(err))
        return
    
    if img_list == []:
        nuke.message(no_nodes_error_msg)
    else:
        sendToMari('mari.system.nuke_bridge.loadImages( %s )' % img_list)
        sendLUT(enable_error=False)

#-------------------------------------------------------------------------------
def createProjector( projector_list ):
    """Creates a projection setup based on the data sent from Mari.
    
    @param projector_list: a list of dictionaries sent from Mari via mari.system.nuke_bridge.exportProjectors().
                    example: [{'name': 'Projector1',
                              'haperture':24.576000000000001,
                              'scale':(0.75976,1.0),
                              'rotate': (1.5607429947874627, 0.46229003819108477, -2.9321485111522581),
                              'img': u'/ohufx/consulting/Foundry/MariNuke/mariData/Camera6_0041.exr',
                              'translate': (2.9500002861022949, 2.1400003433227539, 2.9500002861022949),
                              'focal': 78.999995843413359,
                              'vaperture': 18.672000000000001}, etc...]
    """
    orig_sel = nuke.selectedNodes()
    [ n.setSelected( False ) for n in orig_sel ]
    new_nodes = []
    for proj_data in projector_list:
        scale = proj_data['scale'] if proj_data.has_key('scale') else None
        created_nodes = createRead(proj_data['img'], scale=scale, inpanel=False)
        read_node = created_nodes[0]
        proj_node = nuke.createNode('Project3D', inpanel=False)
        cam_node = nuke.createNode('Camera2', 'rot_order ZXY')
        new_nodes += [ read_node, proj_data, cam_node ]
        
        proj_node.autoplace()
        cam_node.autoplace()
        # The read node is autoplaced in createRead().
        nuke.show( cam_node )
        
        for property in ( 'translate', 'rotate', 'haperture', 'vaperture' ):
            cam_node[property].setValue( proj_data[property] )

        if proj_data['focal']:
            # Perspective cameras
            cam_node['projection_mode'].setValue( 'perspective' )
            cam_node['focal'].setValue( proj_data['focal'] )
        else:
            # Orthographic cameras
            cam_node['projection_mode'].setValue( 'orthographic' )
            cam_node['focal'].setValue( 1 )
            ap = proj_data['orthoScale'] * 2
            cam_node['haperture'].setValue( ap )
            cam_node['vaperture'].setValue( ap )

        cam_node['label'].setValue( 'mari projector\n%s' % proj_data['name'] )
    
    
        proj_node.setInput( 0, created_nodes[-1] )  # connect to the last of the nodes created with the Read
        proj_node.setInput( 1, cam_node )

    return new_nodes

#-------------------------------------------------------------------------------
def createKnob(node, knob_type, name, *args):
    "Creates and adds a knob with the given arguments if it doesn't exist, or if it does exist, just returns it."
    knob = node.knob(name)
    if knob is None:
        knob = knob_type(name, *args)
        node.addKnob(knob)
    return knob

#-------------------------------------------------------------------------------
def createMariTab():
    "Creates a new tab on the root node."
    node = nuke.thisNode()
    debugMsg('%s Mari tab in root' % ("creating" if node.knob('mariTab') is None else "refreshing"))
    
    mari_tab_knob = createKnob(node, nuke.Tab_Knob, 'mariTab', 'Mari')
    
    receive_status_knob = createKnob(node, nuke.Text_Knob, 'cmdStatus', 'listen status', '<b>Disabled</b>')
    receive_status_knob.setTooltip("The status of Nuke's command port")
    receive_status_knob.setFlag(nuke.ENDLINE | nuke.DO_NOT_WRITE)
    
    send_status_knob = createKnob(node, nuke.Text_Knob, 'sendStatus', 'send status', '<b>Inactive</b>')
    send_status_knob.setTooltip("The status of Nuke's connection to Mari")
    send_status_knob.setFlag(nuke.ENDLINE | nuke.DO_NOT_WRITE)
    
    port_knob = createKnob(node, nuke.Int_Knob, 'socketPort', 'nuke command port')
    port_knob.setValue(_default_listen_port)
    port_knob.setTooltip( 'Port to listen on. Make sure this matches the command port set in Mari\'s "Nuke" Palette.' )
    enable_knob = createKnob(node, nuke.Boolean_Knob, 'enableSocket', 'enabled')
    enable_knob.clearFlag( nuke.STARTLINE )
    
    group_knob = createKnob(node, nuke.Tab_Knob, 'advanced', 'advanced', 1)     # 1 = "make it a group knob"
    group_knob.setFlag(1)                                                       # 1 = "group is closed" flag
    
    port_range_knob = createKnob(node, nuke.Int_Knob, 'portRange', 'port range')
    port_range_knob.setValue(_default_port_range)
    port_range_knob.setTooltip("If the main specified command port is unavailable, Nuke will try using the next port number, " + \
                               "and continue until successful or the indicated number of ports have been tried.")
    range_enable_knob = createKnob(node, nuke.Enumeration_Knob, 'enablePortRange', '', ['use range', _single_port_text])
    range_enable_knob.clearFlag(nuke.STARTLINE)
    range_enable_knob.setTooltip("Indicates whether to use a range of ports up to the given number, or to use only the single one specified.")
    
    localhost_knob = createKnob(node, nuke.Boolean_Knob, 'localhostOnly', 'local host only', True)
    localhost_knob.setFlag(nuke.STARTLINE)
    localhost_knob.setTooltip('This determines whether the Mari bridge server will listen for connections from any machine, ' + \
                              'or from "localhost" (the local machine) only.<p>' + \
                              'Only allowing connections from localhost is more secure, but will prevent you from using the ' + \
                              'Nuke&lt;&gt;Mari workflow across the network.')
    
    divider = createKnob(node, nuke.Text_Knob, 'divider', '')
    
    mari_host_knob = createKnob(node, nuke.String_Knob, 'hostName', 'mari host')
    mari_host_knob.setValue('localhost')
    mari_host_knob.setTooltip('The machine name or IP address that Mari is running on.\n' + \
                              'Leave empty if both Mari and Nuke are running on the same machine.')
    
    port_knob_send = createKnob(node, nuke.Int_Knob, 'socketPortSend', 'port')
    port_knob_send.setValue(_default_send_port)
    port_knob_send.setTooltip( "Port that Mari is listening to. Make sure this matches the command port set in Mari's preferences." )
    port_knob_send.clearFlag( nuke.STARTLINE )
    
    mari_data_dir_knob = createKnob(node, nuke.File_Knob, 'mariDataDir', 'mari data dir')
    mari_data_dir_knob.setTooltip('Path to directory that will hold transient data to be sent to Mari (exrs, objs and fbx files). If this is left empty, ' + \
                                  'a "mari" directory will be created in the nk file\'s location')
    mari_data_dir_knob.setValue('[getenv NUKE_TEMP_DIR]/mariData')
    
    mari_location_knob = createKnob(node, nuke.File_Knob, 'mariLocation', 'mari launch path')
    mari_location_knob.setTooltip('The path to launch Mari from.<br>This can also be set using the <b>' + _install_path_var + '</b> environment variable.')
    mari_location_knob.setValue(_mari_path)

#-------------------------------------------------------------------------------
def _rootKnobCreated():
    global _script_loaded
    _script_loaded = True
    loadDefaults()
    
#-------------------------------------------------------------------------------
def _rootKnobAboutToDestroy():
    closeAllConnections()
    global _script_loaded
    _script_loaded = False
    
#-------------------------------------------------------------------------------
def _rootKnobChanged():
    def forcePositiveIntValue(knob, default):
        value = knob.value()
        try:
            if int(value) >= 1:
                return
        except ValueError:
            pass
        knob.setValue(default)
    
    node = nuke.thisNode()
    if node != nuke.root():
        return
    
    knob = nuke.thisKnob()
    try:
        name = knob.name()
    except ValueError:
        debugMsg("Knob '%s' is not attached to a node")
        return
    
    # Handle changes for various knobs
    if name == 'enableSocket':
        toggleConnection(node, knob)
    elif name == 'mariDataDir':
        updateDataDir(knob)
    elif name == 'socketPort':
        forcePositiveIntValue(knob, _default_listen_port)
    elif name == 'portRange':
        forcePositiveIntValue(knob, _default_port_range)
    elif name == 'hostName' or name == 'socketPortSend':
        disconnectFromMari()                # disconnect when changed
        if name == 'socketPortSend':
            checkSendPort()
    elif name == 'mariLocation':
        checkMariLocation()

#-------------------------------------------------------------------------------
def checkSendPort():
    "Validates the port to send data to Mari."
    # Check that we have all the knobs we need
    root = nuke.root()
    try:
        if not all((root.knob(name) is not None and root.knob(name).value() is not None for name in ('socketPort', 'socketPortSend'))):
            return
    except ValueError:      # not attached to a node
        return
    
    # Check that the Nuke and Mari ports aren't the same
    global _actual_port
    global _script_loaded
    send_port = root.knob('socketPortSend').value()
    recv_port = root.knob('socketPort').value()
    if _script_loaded and (send_port == recv_port or send_port == _actual_port):
        nuke.message("<b>Nuke and Mari are set to use the same port (%d).</b>" % send_port + \
                     "<p>The port to use to send data to Mari (\"mari port\" in the \"Mari\" tab of the project settings, under \"advanced\") " + \
                     "must be different from the port used to receive data from Mari (\"command port\" in the \"Mari \" tab of the project " + \
                     "settings)." + \
                     "<p>Please check the configuration and try again.")
        # Turn off the listening connection if it was active
        enable_knob = root.knob('enableSocket')
        if enable_knob.value():
            setConnectionActive(False)

#-------------------------------------------------------------------------------
def updateDataDir(knob):
    "Sets up the data directory."
    if os.path.isfile( knob.value() ):
        knob.setValue( os.path.dirname( knob.value() ) )

#-------------------------------------------------------------------------------
def loadDefaults():
    "Loads the Mari tab into existing scripts."
    global _enable_socket
    if _enable_socket:
        nuke.root()['enableSocket'].setValue( True)

    createMariTab()
    # This works around the fact that loading a script seems to reuse an unused root and its custom knobs,
    # but lose the values assigned in the createMariTab callback on script load.
    debugMsg('loading values into Mari tab')
    def_values = { 'socketPort': _default_listen_port, 'socketPortSend': _default_send_port, 'mariDataDir': '[file dirname [value root.name]]/mariData' }
    root = nuke.root()
    for knob, value in def_values.iteritems():
        if not root[knob].value():
            root[knob].setValue(value)

#-------------------------------------------------------------------------------
def importMNB():
    mnb_file = nuke.getFilename( 'Load Mari Projection', '*.mnb')
    if mnb_file:
        with open( mnb_file, 'r' ) as data_file:
            data_set = pickle.load( data_file )
            createProjector( data_set )

#-------------------------------------------------------------------------------
def findFirstActiveNode(node):
    "Returns the first 'active' (non-Dot or NoOp) node found, starting from the given one, or None."
    # NoOps and Dots have no Ops inside them, so opHashes will be an empty list
    while node is not None and len(node.opHashes()) == 0:
        node = node.input(0)
    return node

#-------------------------------------------------------------------------------
def filenameFilter( path ):
    """Modifies the path so it is a valid file path on the machine that runs Mari.
    
    Overwrite this function to customise.
    Example in Nuke's menu.py:
    def nukeMacToMariLinux( path ):
       return path.replace( '/Volumes/', '/' )
    mari_bridge.filenameFilter = nukeMacToMariLinux
    """
    return path
    
# ------------------------------------------------------------------------------
def init():
    "Initialises the Mari bridge in Nuke."
    # Set up callbacks
    debugMsg('Initialising callbacks')
    nuke.addOnCreate(_rootKnobCreated, nodeClass='Root')
    nuke.addOnDestroy(_rootKnobAboutToDestroy, nodeClass='Root')
    nuke.addKnobChanged(_rootKnobChanged, nodeClass='Root')
    
    # Set up menus
    nuke.pluginAddPath('./icons')
    menubar = nuke.menu('Nuke').addMenu('&Mari')
    toolbar = nuke.toolbar('&Mari')
    for menu in ( menubar, toolbar ):
        menu.addCommand(        '&Launch Mari',             launchMari, icon='MariIcon.png')
        menu.addCommand(        '&Import Projection',       importMNB, icon='FolderIcon')
        
        send_menu = menu.addMenu('&Send', icon='Output.png' )
        send_menu.addCommand(   '&Projection Components',   lambda: checkAndCall("exportProjectors(use_socket=True)"), icon='Camera.png')
        send_menu.addCommand(   '&Sequence Projections',    lambda: checkAndCall("exportProjectors(use_socket=True, sequence=True)"), icon='CameraShake.png')
        send_menu.addSeparator()
        
        image_menu = send_menu.addMenu('&Images', icon='Read.png')
        image_menu.addCommand(  'All &Read Nodes',          lambda: checkAndCall("sendNodes(nuke.allNodes('Read'), 'No Read nodes available.')"))
        image_menu.addCommand(  '&Selected Read Nodes',     lambda: checkAndCall("sendNodes(nuke.selectedNodes('Read'), 'No Read nodes selected.')"))
        image_menu.addSeparator()
        image_menu.addCommand(  'Selected &Nodes',          lambda: checkAndCall("sendNodes(nuke.selectedNodes(), 'No nodes selected.')"))
        
        send_menu.addSeparator()
        send_menu.addCommand(   '&LUT',                     lambda: checkAndCall("sendLUT()"), icon='ColorLookup.png')
        
        export_menu = menu.addMenu('&Export', icon='DiskCache.png')
        export_menu.addCommand( '&Projection(s)...',        exportProjectors, icon='Camera.png')
        export_menu.addCommand( '&Sequence Projections...', lambda: exportProjectors(sequence=True), icon='CameraShake.png')

# ------------------------------------------------------------------------------

init()
