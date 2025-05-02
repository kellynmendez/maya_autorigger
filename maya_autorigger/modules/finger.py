#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez

:synopsis:
    This module contains the class for creating a finger component.
"""
from turtledemo.penrose import start

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in

# Third party
import maya.cmds as cmds

# Internal
from maya_autorigger.modules.rig_base import BaseComponent
from maya_autorigger.utils.enums import SIDE, AXIS
from maya_autorigger.utils.rig_utils import create_locator_chain


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class FingerComponent(BaseComponent):
    """
    Base class for a rig component
    """
    def __init__(self, name, start_pos, num_joints=3, length=1, side=SIDE.C, axis=AXIS.X):
        """
        :param name: Name of joint
        :type: str

        :param num_joints: Number of joints in chain
        :type: int

        :param length: Length of chain
        :type: float

        :param start_pos: Starting position of chain
        :type: tuple

        :param side: Direction to build chain
        :type: gen_utils.SIDE

        :param axis: Axis to build chain along
        :type: gen_utils.AXIS
        """
        super().__init__(name)
        self.num_joints = num_joints
        self.length = length
        self.start_pos = start_pos
        self.side = side
        self.axis = axis


    def create_locators(self):
        """
        Creates the base locators for finger
        """
        # Determine directional vector
        if self.axis == AXIS.X:
            dir_vector = (1, 0, 0)
        elif self.axis == AXIS.Y:
            dir_vector = (0, 1, 0)
        else:
            dir_vector = (0, 0, 1)
        if self.side == SIDE.R:
            dir_vector *= -1

        self.locators = create_locator_chain(self.name, self.side, dir_vector,
                                             self.num_joints, self.length,
                                             self.start_pos)
        
    
    def build(self):
        """
        Builds finger rig
        """


    def create_ctrls(self):
        """
        Creates the curve controls for the finger
        """

