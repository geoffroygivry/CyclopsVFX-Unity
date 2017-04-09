import re
import nuke

def addStores( node, amount ):
    '''
    Add the Stores tab to a node and add as many store buttons as 
       args:
          node   -   node to add stores to
          amount -   number of stores to add
    '''
    node.addKnob( nuke.Tab_Knob('Stores') )
    defCode = 'nuke.message("Empty store.\\nUse right click menu to save values to store.")'
    for store in range ( amount ):
        store += 1
        k = nuke.PyScript_Knob( 'store'+str(store), '<i><small>Store '+ str(store), defCode)
        node.addKnob( k )
    
def saveStore( node, store, maxStores, excludeKnobs=[] ):
    '''
    Save the current node values in the specified store. If stores dont exist yet they will be created.
    args:
       node           -   node object to operate on
       store          -   knob name of store to save values to
       excludeKnobs   -   knobs to exculde from being saved in a store
    '''
    if not 'Stores' in node.knobs().keys():
        addStores( node, maxStores )
    sKnob = node[ store ]
    # GET VALUES AND WRITE THEM TO REQUESTED STORE
    knobValues = node.writeKnobs( nuke.TO_SCRIPT )
    # MANUALLY EXCLUDE KNOBS FROM BEING RECORDED
    exclude = [k for k in node.knobs() if k.startswith( 'store' )] + excludeKnobs
    for e in exclude:
        knobValues = re.sub( r'%s\s.+\n?' % e, '', knobValues )
    print 'saving to store %s:\n%s' % ( store, knobValues )
    code = 'nuke.thisNode().readKnobs( \'\'\'%s\'\'\' )' % knobValues
    sKnob.setValue( code )
    # SET TOOLTIP TO USER DESCRIPTION
    curTip = sKnob.tooltip()
    defaultTip = curTip[ curTip.find('>')+1 : curTip.rfind('<') ]
    toolTip = nuke.getInput('tooltip for ' +store, defaultTip)
    sKnob.setTooltip( '<b>%s</b>\n%s' % (toolTip, knobValues) )
    # UPDATE LABEL FORMAT
    cleanLabel = sKnob.label()[sKnob.label().rindex('>')+1:]
    sKnob.setLabel( '<b>'+cleanLabel )

    
def addStoresMenu( amount=3, excludeKnobs=[] ):
    '''
    Add the Stores into the property panel's right click menu.
       args:
          amount        -   how many stores to use
          excludeKnobs  -   list of knob names to exclude from being saved to a store
    '''
    for i in range( amount ):
        i += 1
        nuke.menu('Properties').addCommand('Stores/load store %s' % i, 'nuke.selectedNode()["store%s"].execute()' % i )
    nuke.menu('Properties').findItem('Stores').addSeparator()
    for i in range( amount ):
        i += 1
        nuke.menu('Properties').addCommand('Stores/save in store %s' % i, 'stores.saveStore( nuke.selectedNode(), "store%s", %s, %s )' % (i, amount, excludeKnobs) )
    
    
