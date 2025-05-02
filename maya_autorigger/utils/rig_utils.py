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
from utils.gen_utils import SUFFIX

# Internal

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
    vector_incr = dir_vector * gap

    for loc_num in range(num_joints):
        loc_name = f'{side}_{name}{num_joints - loc_num}_{SUFFIX.LOC}'
        loc = cmds.spaceLocator(name=loc_name, position=next_pos)
        locators.append(loc)
        next_pos += vector_incr

    return locators



#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#