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
     # Get variables for making component
    module = attributes[TEMPLATE_KEY.MODULE]
    num_comps = int(attributes[TEMPLATE_KEY.NUM_COMPS])
    side = attributes[TEMPLATE_KEY.SIDE]
    num_joints = int(attributes[TEMPLATE_KEY.NUM_JOINTS])
    axis = getattr(AXIS, attributes[TEMPLATE_KEY.AXIS])

    # Set the start position based on previous lengths
    start_pos = (0, 0, 0)
    if distance != 0:
        if side == SIDE.R:
            add = multipy_tup(axis, distance * -1)
        else:
            add = multipy_tup(axis, distance)
        start_pos = add_tup(start_pos, add_tup(add, multipy_tup(axis, DEFAULT_LENGTH.Spacer)))

    # Determine spread axis
    if axis == AXIS.X:
        spread_axis = AXIS.Z
    else:
        spread_axis = AXIS.X

    comps = []
     # Create given number of components
    for i in range(1, num_comps + 1):
        if num_comps == 1:  # Only one component made
            name = f'{module.lower()}'
            position = start_pos
        elif i == 1:        # First component should have original start position
            name = f'{module.lower()}{i:02d}_'
            position = start_pos
        else:               # Alternate either side after first component
            name = f'{module.lower()}{i:02d}_'
            direction = (-1) ** i               # +1, -1, +1, -1...
            step = ((i - 2) // 2 + 1) * 2       # 2, 2, 4, 4, 6, 6, ...
            offset = multipy_tup(spread_axis, direction * step)
            position = add_tup(start_pos, offset)

        print(position)
        comps.append(globals()[module](name=name,
                                       side=side,
                                       start_pos=position,
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

        #
        self.components = []
        for key in template_dict.keys():
            self.components.extend(self._create_locator_helper(template_dict[key]))

        parent = None
        for comp in self.components:
            if not parent:
                parent = comp
                continue
            comp.set_parent(parent, loc_flag=True)


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
        parent = None
        for comp in self.components:
            comp.build()
            if not parent:
                parent = comp
                continue
            comp.set_parent(parent, loc_flag=False)