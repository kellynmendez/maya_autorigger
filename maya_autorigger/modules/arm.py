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
from maya_autorigger.modules.base_comp import Component
from maya_autorigger.utils.enums import JNT_NAME, SUFFIX
from maya_autorigger.utils.maya_utils import create_locator_chain

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

    def create_locators(self):
        """
        Creates the base locators for arm
        """
        self.locators = create_locator_chain(name=self.loc_name,
                                             num_joints=self.num_joints,
                                             length=self.length,
                                             dir_vector=self.dir_vector,
                                             start_pos=self.start_pos)

    def create_ctrls(self):
        """
        Creates the curve controls for the ar,
        """