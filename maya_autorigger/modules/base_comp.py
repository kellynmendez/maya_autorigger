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
from maya_autorigger.utils.enums import SIDE
from maya_autorigger.utils.maya_utils import multipy_tup


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
        # Parent is set later
        self.parent = None

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

    @abstractmethod
    def build(self):
        """
        Builds the joints from the locators
        """
        raise NotImplementedError("Subclass must implement build method.")

    @abstractmethod
    def create_ctrls(self):
        """
        Creates the curve controls for the component
        """
        raise NotImplementedError("Subclass must implement create_ctrls method.")

    def get_root(self, loc_flag):
        """
        Get root of chain
        """
        if loc_flag:
            return self.locators[0]
        else:
            return self.joints[0]

    def get_end(self, loc_flag):
        """
        Get root of chain
        """
        if loc_flag:
            return self.locators[-1]
        else:
            return self.joints[-1]

    def set_parent(self, parent, loc_flag):
        """
        Sets the parent of the joint
        """
        self.parent = parent
        cmds.parent(self.get_root(loc_flag=loc_flag), parent.get_end(loc_flag=loc_flag))