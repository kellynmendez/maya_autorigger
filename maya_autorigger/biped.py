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
import os

# Third party

# Internal
from maya_autorigger.modules.finger import FingerComponent
from maya_autorigger.modules.hand import HandComponent
from maya_autorigger.modules.arm import ArmComponent
from maya_autorigger.utils.enums import SIDE, AXIS, COMP
from maya_autorigger.utils.gen_utils import read_xml


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Biped:
    """
    Builds the rig using the modules
    """
    def __init__(self, arm_jnt_num):
        """
        :param arm_jnt_num: Number of joints in the arm
        :type: int
        """
        self.template = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                     "templates\\arm.xml")
        self.arm_jnt_num = arm_jnt_num

    def build_rig(self):
        """
        Builds the rig module by module
        """
        # This builds just the arm for now
        template_dict = read_xml(self.template)

    def _build_rig_helper(self, curr_level):
        """

        :param curr_level:
        :return:
        """
