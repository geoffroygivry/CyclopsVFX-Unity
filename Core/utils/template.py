#! /usr/bin/env python
# This free software incorporates by reference the text of the WTFPL, Version 2

"""
This is where your module level help string goes.

.. module:: `dummy`
   :platform: Unix, Windows
   :synopsis: Put a synopsis of what this module does here.

.. moduleauthor:: Michael Morehouse <michael@yawpitchroll.com>
"""

# IMPORT STANDARD MODULES
# import standard modules here

# IMPORT LOCAL MODULES
from terminallogger import get_terminal_logger

LOGGER = get_terminal_logger(__name__)

class MyDummyClass(object):
    def __init__(self, *args, **kwargs):
        super(MyDummyClass, self).__init__(*args, **kwargs)
    # end __init__
    
    def some_method(self):
        """
        If the record does is not logging.INFO, return True
        """
        pass
    # end some_method
# end MyDummyClass

def my_dummy_function():
    """
    Help string that describes my_dummy_function
    
    :arg somearg: describe what somearg is
    :type somearg: type of somearg
    :returns: what this function returns
    :rtype: type of the returned object
    """
    pass
# end my_dummy_function

def main():
    """
    Simply run help if called directly.
    """
    import __main__
    help(__main__)
# end main

__all__ = ['MyDummyClass', 'my_dummy_function']

if __name__ == '__main__':
    main()
    
