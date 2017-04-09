# ------------------------------------------------------------------------------
# Mari-Nuke communication scripts
# - Nuke's server for communication with Mari
# 
# coding: utf-8
# Copyright (c) 2011 The Foundry Visionmongers Ltd.  All Rights Reserved.
# ------------------------------------------------------------------------------

import nuke
import socket
import threading

_nuke_exec_cmd = "nukeDo:"
_nuke_eval_cmd = "nukeEval:"

#-------------------------------------------------------------------------------
# _ServerThread
#-------------------------------------------------------------------------------
class _ServerThread(threading.Thread):
    def __init__(self, receiver):
        super(_ServerThread, self).__init__()
        self.setDaemon(True)
        self._receiver = receiver
        
    #-------------------------------------------------------------------------------
    def run(self):
        setSocketKnobState(True)
        debugMsg('Server thread started')
        
        try:
            self._exec()
        except socket.error as err:
            # Check for the 'bad file descriptor' error, which means the socket has been closed
            if err[0] == 9:
                debugMsg('Socket closed')
            elif err[0] == 4:
                debugMsg('Socket error: interrupted system call')
            else:
                errorMsg("Unhandled socket error in Mari bridge server thread: " + str(err))
        except Exception as exc:
            errorMsg("Unhandled exception in Mari bridge server thread: " + str(exc))
        
        setSocketKnobState(False)
        debugMsg('Exiting server thread')
    
    #-------------------------------------------------------------------------------
    def _exec(self):
        self._receiver.settimeout(0.01)
        debugMsg('Server running on ' + str(self._receiver.getsockname()))
        
        connections = []
        READ_LENGTH = 1024
        
        # Main loop: check for new connections, and process data from them
        while True:
            # Accept pending incoming connections
            try:
                new_conn, details = self._receiver.accept()
                new_conn.settimeout(0.01)
                debugMsg('New connection on ' + str(details))
                connections.append(new_conn)
            except socket.timeout:
                pass
            except socket.error as err:
                if err[0] != 4:     # ignore "interrupted system call" (retry next loop)
                    raise
            
            # Check each open connection for new data
            for conn in list(connections):  # make a copy so we can safely modify the original
                data_block = ''
                # Receive data while some is available and we don't have an error
                while True:
                    # Receive data
                    try:
                        new_data = conn.recv(READ_LENGTH)
                    except socket.timeout:
                        break
                    except Exception as exc:
                        errorMsg("Closing connection due to unhandled exception in socket receive: " + str(exc))
                        connections.remove(conn)
                        break
                    
                    # Receiving an empty string means the socket has been closed - but we may still have data to process
                    if new_data == '':
                        debugMsg('Closing ' + str(conn.getpeername()))
                        connections.remove(conn)
                        break
                    
                    # Append to previously received data, and continue receiving if we got less than a buffer full
                    data_block += new_data
                    if len(new_data) < READ_LENGTH:
                        break
                
                # Loop through all segments to process, using Ctrl+D as an optional delimiter
                data_segments = (text for text in data_block.split('\x04') if text != "")
                for data in data_segments:
                    
                    # Debug info
                    trace_text = data[:100]
                    if len(data) > len(trace_text):
                        trace_text += "..."
                    debugMsg("Received: " + trace_text)
                    
                    if data.startswith(_nuke_exec_cmd):
                        # Received an execute command
                        request = data.replace(_nuke_exec_cmd, '')
                        debugMsg('Executing in Nuke')
                        # Request a result (but ignore it) to ensure that the command finishes before returning
                        nuke.executeInMainThreadWithResult(runPython, request)
                        
                    elif data.startswith(_nuke_eval_cmd):
                        # Received an evaluate command
                        request = data.replace(_nuke_eval_cmd, '')
                        debugMsg('Evaluating in Nuke')
                        result = str(nuke.executeInMainThreadWithResult(evalPython, request))
                        debugMsg('Sending: %s' % result)
                        try:
                            conn.send(result)
                            debugMsg('Send complete')
                        except socket.timeout:
                            debugMsg('Send timed out')
                        except socket.error as err:
                            if err[0] == 32 or err[0] == 104:
                                # Broken pipe or connection reset by peer => closed (ignore; will be removed next check)
                                debugMsg('Send cancelled (connection closed)')
                            else:
                                raise
                    
                    elif data == ':exit:':
                        # Received a request to close the connection
                        debugMsg('Close connection requested by ' + str(conn.getpeername()))
                        self._receiver.close()
                        return

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def errorMsg(message):
    "Prints an error message to the terminal and script editor output."
    message = str(message)
    nuke.tprint(message)
    print message

#-------------------------------------------------------------------------------
def debugMsg(message):
    "Traces debugging messages, if enabled."
    if debugMsg._enabled:
        errorMsg(message)

debugMsg._enabled = False

#-------------------------------------------------------------------------------
def setDebug(enabled):
    "Enables or disables debugging messages."
    debugMsg._enabled = enabled

#-------------------------------------------------------------------------------
def runPython(cmd):
    """Executes the incoming Python commmand in Nuke.
    
    @param cmd: Python command
    @type  cmd: str
    """
    import mari_bridge
    try:
        exec cmd.strip()
    except:
        # Catch everything and report
        import traceback
        mari_bridge.errorMsg(traceback.format_exc())

#-------------------------------------------------------------------------------
def evalPython(cmd):
    """Evaluates the incoming Python commmand in Nuke, and returns the result.
    
    @param cmd:     Python command
    @type  cmd:     str
    @return:        The result of the command
    @rtype:         variant (may be any type, including None)
    @raise None:    All exceptions are caught and printed out
    """
    import mari_bridge
    try:
        return eval(cmd.strip())
    except:
        # Catch everything and report; implicitly return None
        import traceback
        mari_bridge.errorMsg(traceback.format_exc())

#-------------------------------------------------------------------------------
def setSocketKnobState(active):
    """Turns on or off the 'enable socket' knob on the Mari tab.
    
    @param active: True or False
    """
    def setStates(active):
        root = nuke.root()
        root['enableSocket'].setValue(active)
        root['socketPort'].setEnabled(not active)
    
    nuke.executeInMainThread(lambda: setStates(active))

#-------------------------------------------------------------------------------
def serve(port, localhost_only):
    _max_clients = 10
    _connector = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    # Allow the re-using of addresses when appropriate.
    # - On Linux, this means you can toggle off and on and get the same address
    # - On Windows, this means anything can use the same address, and causes problems.  Toggling off and on works fine anyway
    if not nuke.env['WIN32']:
        _connector.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Try to bind
    try:
        debugMsg("Binding to %s on port %d" % ('localhost' if localhost_only else 'any local address', port))
        bind_address = 'localhost' if localhost_only else ''    # '' = any local address (e.g. 'localhost' or host name)
        _connector.bind((bind_address, port))

    except socket.error as err:
        # Check if the port was in use
        if err[0] == 98 or err[0] == 10048:         # in use, on Linux or Windows
            msg = "Port " + str(port) + " in use"
            debugMsg(msg)
            raise ValueError(msg)
        # Unknown socket error
        raise

    _connector.listen(int(_max_clients))
    _ServerThread(_connector).start()

#-------------------------------------------------------------------------------
def stopConnection( port ):
    "Tells the Mari bridge server to stop."
    # Ignore missing or invalid port numbers
    if port is None or port == "":
        return
    try:
        port = int(port)
    except ValueError:
        return
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect( ( 'localhost', port ) )
        s.send( ':exit:' )

    except socket.error as err:
        # If the connection was refused, assume there was no Mari bridge server to tell to exit
        if err[0] == 111:   # connection refused
            debugMsg('Mari bridge server already stopped')
        else:
            # Unknown socket error
            raise

#-------------------------------------------------------------------------------
