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
import maya.cmds as cmds

# Internal
from maya_autorigger.utils.enums import SIDE, SUFFIX
from maya_autorigger.utils.maya_utils import multipy_tup, create_joints_from_locators


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Component:
    """
    Base class for a rig component
    """
    def __init__(self, name, side, start_pos, num_joints, length, axis):
        """
        :param name: Name of this component
        :type: str

        :param side: Prefix for side finger is on
        :type: utils.enums.SIDE

        :param start_pos: Starting position of chain
        :type: tuple

        :param num_joints: Number of joints in chain
        :type: int

        :param length: Length of chain
        :type: float

        :param axis: Axis to build chain along
        :type: utils.enums.AXIS
        """
        # Class vars
        self.name = name
        self.side = side
        self.start_pos = start_pos
        self.num_joints = num_joints
        self.length = length

        # Lists to track
        self.locators = []
        self.joints = []
        self.controls = []

        # Determine directional vector
        self.dir_vector = axis
        if self.side == SIDE.R:
            self.dir_vector = multipy_tup(axis, -1)

    @abstractmethod
    def create_locators(self):
        """
        Creates the base locators for finger
        """
        raise NotImplementedError("Subclass must implement create_locators method.")

    def build(self):
        """
        Builds the joints from the locators
        """
        self.joints = create_joints_from_locators(self.locators)

    @abstractmethod
    def create_ctrls(self):
        """
        Creates the curve controls for the component
        """
        raise NotImplementedError("Subclass must implement create_ctrls method.")

    def get_root(self):
        """
        Get root of chain
        """
        return self.locators[0]

    def get_end(self):
        """
        Get root of chain
        """
        print(self.locators)
        return self.locators[-1]

    def set_parent(self, parent):
        """
        Sets the parent of the joint
        """
        cmds.parent(self.get_root(), parent)