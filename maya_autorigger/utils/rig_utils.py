#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez

:synopsis:
    This module contains utilities for working with rigs in maya.
"""


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in

# Third party
import maya.cmds as cmds

# Internal
from maya_autorigger.utils.enums import SUFFIX
from maya_autorigger.utils.gen_utils import multipy_tup, add_tup


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def create_locator_chain(name, side, dir_vector, num_joints=3, length=6,
                         start_pos=(0, 0, 0)):
    """
    Creates a chain of locators
    """
    locators = []
    next_pos = start_pos
    gap = length / num_joints
    vector_incr = multipy_tup(dir_vector, gap)

    for loc_num in range(1, num_joints):
        loc_name = f'{side}_{name}{loc_num:02}_{SUFFIX.LOCATOR}'
        loc = cmds.spaceLocator(name=loc_name, position=next_pos)
        locators.append(loc)
        next_pos = add_tup(next_pos, vector_incr)

    for loc_num in range(1, len(locators)):
        cmds.parent(locators[loc_num], locators[loc_num - 1])

    return locators



#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#