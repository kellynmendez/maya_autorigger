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
from modules.rig_base import BaseComponent

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class ArmComponent(BaseComponent):
    """
    Base class for a rig component
    """

    def __init__(self, name):
        super().__init__(name)

    def create_locators(self):
        """
        Creates the base locators for hand
        """

    def build(self):
        """
        Builds hand rig
        """

    def create_ctrls(self):
        """
        Creates the curve controls for the hand
        """