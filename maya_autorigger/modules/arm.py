#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez

:synopsis:
    This module contains the class for creating an arm component.
"""


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in

# Third party

# Internal
from maya_autorigger.modules.base_comp import BaseComponent
from maya_autorigger.utils.enums import SIDE, AXIS
from maya_autorigger.utils.maya_utils import (create_locator_chain,
                                              create_joints_from_locators)

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class ArmComponent(BaseComponent):
    """
    Base class for a rig component
    """
    def __init__(self, name, side, start_pos, num_joints=3, length=1, axis=AXIS.X):
        """
        :param name: Name of joint
        :type: str

        :param side: Prefix for side arm is on
        :type: utils.enums.SIDE

        :param num_joints: Number of joints in chain
        :type: int

        :param length: Length of chain
        :type: float

        :param start_pos: Starting position of chain
        :type: tuple

        :param axis: Axis to build chain along
        :type: utils.enums.AXIS
        """
        super().__init__(name, side)
        self.num_joints = num_joints
        self.length = length
        self.start_pos = start_pos
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

        self.locators = create_locator_chain(name=self.name,
                                             side=self.side,
                                             dir_vector=dir_vector,
                                             num_joints=self.num_joints,
                                             length=self.length,
                                             start_pos=self.start_pos)


    def build(self):
        """
        Builds finger rig
        """
        create_joints_from_locators(self.locators)


    def create_ctrls(self):
        """
        Creates the curve controls for the finger
        """