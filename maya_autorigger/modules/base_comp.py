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

class BaseComponent:
    """
    Base class for a rig component
    """
    def __init__(self, name, side):
        self.name = name
        self.side = side
        self.locators = []
        self.joints = []
        self.controls = []

    @abstractmethod
    def create_locators(self):
        """
        Creates the base locators for rig component
        """
        raise NotImplementedError("Subclass must implement create_locs method.")

    @abstractmethod
    def build(self):
        """
        Builds rig component
        """
        raise NotImplementedError("Subclass must implement build method.")

    @abstractmethod
    def create_ctrls(self):
        """
        Creates the curve controls for the component
        """
        raise NotImplementedError("Subclass must implement create_ctrls method.")

    def get_root(self):
        """
        Gives component that should be connected

        :return: Root component that should be connected to parent
        :type: 
        """
        return self.joints[0]