#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez

:synopsis:
    This module contains the base class for creating a rig component.
"""


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in
from abc import abstractmethod

# Third party

# Internal

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class BaseRigComponent:
    """
    Base class for a rig component
    """
    def __init__(self, name):
        self.name = name
        self.joints = []
        self.controls = []
        self.root = None

    @abstractmethod
    def build(self):
        """
        Builds rig component
        """
        raise NotImplementedError("Subclass must implement build method.")

    @abstractmethod
    def connect(self, parent=None):
        """
        Connects component to next component
        """
        raise NotImplementedError("Subclass must implement connect method.")

    @abstractmethod
    def create_ctrls(self):
        """
        Creates the curve controls for the component
        """
        raise NotImplementedError("Subclass must implement create_ctrls method.")
