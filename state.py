# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:25:24 2020

@author: adam
"""


# state.py

class State(object):
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def __init__(self):
        print ("Processing current state:"), str(self)
        #print 'processing current state', str(self)

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__