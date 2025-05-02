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
from shutil import posix

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

    :param name: name of component
    :type: str

    :param side: side prefix
    :type: utils.enums.SIDE

    :param dir_vector: direction to make chain
    :type: tuple

    :param num_joints: number of joints in chain
    :type: int

    :param length: length of the chain
    :type: float

    :param start_pos: position of first joint
    :type: tuple

    :return: list of locators in hierarchical order
    :type: list
    """
    locators = []
    # Starting values
    next_pos = start_pos
    gap = length / num_joints
    vector_incr = multipy_tup(dir_vector, gap)

    # For each joint that we want, create a locator and increment distance
    for loc_num in range(1, num_joints + 1):
        loc_name = f'{side}_{name}{loc_num:02}_{SUFFIX.LOCATOR}'
        loc = cmds.spaceLocator(name=loc_name)[0]
        cmds.xform(loc, worldSpace=True, translation=next_pos)
        locators.append(loc)
        next_pos = add_tup(next_pos, vector_incr)
    # Parent locators down the list
    for loc_num in range(1, len(locators)):
        cmds.parent(locators[loc_num], locators[loc_num - 1])
    # Clear selection
    cmds.select(clear=True)

    return locators

def orient_joint(target_jnt, jnt):
    """

    :param target_jnt:
    :param jnt:
    :return:
    """
    cmds.aimConstraint(target_jnt, jnt, aimVector=(1, 0, 0), upVector = (0, 1, 0))

def create_joints_from_locators(locators):
    """

    :param locators:
    :type: list

    :return: list of joints in hierarchical order
    """
    joints = []
    for i, loc in enumerate(locators):
        # Get position and name
        jnt_name = loc.replace(SUFFIX.LOCATOR, SUFFIX.JOINT)
        # Create joint at origin and with no parent
        jnt = cmds.joint(name=jnt_name)
        if cmds.listRelatives(jnt, parent=True):
            cmds.parent(jnt, world=True)
        # Parent to locator, zero out translation, unparent
        cmds.parent(jnt, loc)
        cmds.xform(jnt, translation=(0, 0, 0))
        cmds.parent(jnt, world=True)
        # Add joint to list
        joints.append(jnt)

        # Parent this joint to the previous one
        if i > 0:
            print(joints)
            cmds.parent(joints[i], joints[i - 1])

    cmds.delete(locators)
    return joints



#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#