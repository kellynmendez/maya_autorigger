#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez

:synopsis:
    This module contains the class for creating a hand component.
"""


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in

# Third party

# Internal
from maya_autorigger.modules.base_comp import BaseComponent

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class HandComponent(BaseComponent):
    """
    Base class for a rig component
    """

    def __init__(self, name, side, length, start_pos):
        super().__init__(name, side)
        """
        :param name: Name of joint
        :type: str

        :param side: Prefix for side finger is on
        :type: utils.enums.SIDE

        :param length: Length of chain
        :type: float

        :param start_pos: Starting position of chain
        :type: tuple
        """
        self.num_joints = 1 # only joint in hand will be palm joint
        self.length = length
        self.start_pos = start_pos

    def create_locators(self):
        """
        Creates the base locator for hand
        """
        self.locators = create_locator_chain(name=self.name,
                                             side=self.side,
                                             num_joints=self.num_joints,
                                             length=self.length,
                                             start_pos=self.start_pos)

    def build(self):
        """
        Builds hand rig
        """
        create_joints_from_locators(self.locators)


    def create_ctrls(self):
        """
        Creates the curve controls for the hand
        """