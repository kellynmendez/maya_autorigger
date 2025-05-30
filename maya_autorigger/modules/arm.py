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
import maya.cmds as cmds

# Internal
from maya_autorigger.modules.base_comp import Component
from maya_autorigger.utils.maya_utils import (create_locator_chain,
                                              create_joints_from_locators,
                                              create_arm_blend_chain)

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Arm(Component):
    """
    Base class for a rig component
    """
    def __init__(self, name, side, start_pos, num_joints, length, axis):
        """
        :param name: Name of this component
        :type: str

        :param side: Prefix for side arm is on
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
        super().__init__(name, side, start_pos, num_joints, length, axis)
        self.blend_jnts = None
        self.fk_jnts = None
        self.ik_jnts = None

    def create_locators(self):
        """
        Creates the base locators for arm
        """
        self.locators = create_locator_chain(name=self.name,
                                             side=self.side,
                                             num_joints=self.num_joints,
                                             length=self.length,
                                             dir_vector=self.dir_vector,
                                             start_pos=self.start_pos)
        return self.locators

    def build(self):
        """
        Builds the joints from the locators
        """
        # Create all joints
        self.fk_jnts = create_joints_from_locators(self.locators, name_modifier='fk')
        self.ik_jnts = create_joints_from_locators(self.locators, name_modifier='ik')
        self.blend_jnts = create_joints_from_locators(self.locators, name_modifier='blend')
        self.joints = self.blend_jnts

        create_arm_blend_chain(self.blend_jnts, self.fk_jnts, self.ik_jnts)


    def create_ctrls(self):
        """
        Creates the curve controls for the ar,
        """