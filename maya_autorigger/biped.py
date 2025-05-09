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
from re import template
from turtledemo.penrose import start

# Third party

# Internal
from maya_autorigger.modules.finger import Finger
from maya_autorigger.modules.arm import Arm
from maya_autorigger.utils.enums import AXIS, SIDE, TEMPLATE_KEY, DEFAULT_LENGTH
from maya_autorigger.utils.gen_utils import read_xml
from maya_autorigger.utils.maya_utils import multipy_tup, add_tup


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def build_component(attributes, distance):
    """

    :return:
    """
    module = attributes[TEMPLATE_KEY.MODULE]
    num_comps = int(attributes[TEMPLATE_KEY.NUM_COMPS])
    side = attributes[TEMPLATE_KEY.SIDE]
    num_joints = int(attributes[TEMPLATE_KEY.NUM_JOINTS])
    axis = getattr(AXIS, attributes[TEMPLATE_KEY.AXIS])

    start_pos = (0, 0, 0)
    if distance != 0:
        if side == SIDE.R:
            add = multipy_tup(axis, distance * -1)
        else:
            add = multipy_tup(axis, distance)
        start_pos = add_tup(start_pos, add_tup(add, multipy_tup(axis, DEFAULT_LENGTH.Spacer)))

    comps = []
    for i in range(1, num_comps + 1):
        if num_comps == 1:
            name = f'{module.lower()}'
        else:
            name = f'{module.lower()}{i:02d}_'
        comps.append(globals()[module](name=name,
                                       side=side,
                                       start_pos=start_pos,
                                       num_joints=num_joints,
                                       length=getattr(DEFAULT_LENGTH, module),
                                       axis=axis))

    # Actually create locators
    for comp in comps:
        comp.create_locators()

    return comps


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Biped:
    """
    Builds the rig using the modules
    """
    def __init__(self, arm_jnt_num, template_file):
        """
        :param arm_jnt_num: Number of joints in the arm
        :type: int
        """
        self.template = template_file
        self.arm_jnt_num = arm_jnt_num
        self.components = []

    def create_locators(self):
        """
        Builds the locators module by module
        """
        # This builds just the arm for now
        template_dict = read_xml(self.template)

        self.components = []
        for key in template_dict.keys():
            self.components.extend(self._create_locator_helper(template_dict[key]))
        print(self.components)
        parent = None
        for comp in self.components:
            print(comp)
            if not parent:
                parent = comp.get_end()
                continue
            print(f'{parent}, {comp}')
            comp.set_parent(parent)

        print(self.components)

    def _create_locator_helper(self, curr_level, distance=0):
        """

        :param curr_level:
        :return:
        """
        components = []

        for key, value in curr_level.items():
            if key == TEMPLATE_KEY.INFO:
                components.extend(build_component(value, distance))
                continue
            elif key == TEMPLATE_KEY.CHILDREN:
                for child in value.keys():
                    distance = getattr(DEFAULT_LENGTH,
                                       curr_level[TEMPLATE_KEY.INFO][TEMPLATE_KEY.MODULE])
                    components.extend(self._create_locator_helper(value[child], distance=distance))

        return components

    def create_joints(self):
        """

        :return:
        """
        for comp in self.components:
            comp.build()