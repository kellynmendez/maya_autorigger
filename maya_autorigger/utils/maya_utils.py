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

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def multipy_tup(tup, scalar):
    return [scalar * t for t in tup]


def add_tup(tup_a, tup_b):
    return [tup_a[i] + tup_b[i] for i in range(3)]


def create_locator_chain(name, side, num_joints, length, dir_vector=None,
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
    gap = length / (num_joints - 1)
    vector_incr = multipy_tup(dir_vector, gap)

    # For each joint that we want, create a locator and increment distance
    for loc_num in range(1, num_joints + 1):
        loc_name = f'{side}_{name}{loc_num:02d}_{SUFFIX.LOCATOR}'
        loc = cmds.spaceLocator(name=loc_name)[0]
        cmds.xform(loc, worldSpace=True, translation=next_pos)
        locators.append(loc)
        if num_joints > 1:
            next_pos = add_tup(next_pos, vector_incr)
    # Parent locators down the list
    for loc_num in range(1, len(locators)):
        cmds.parent(locators[loc_num], locators[loc_num - 1])
    # Clear selection
    cmds.select(clear=True)

    return locators

def create_joints_from_locators(locators, name_modifier=None):
    """

    :param locators:
    :type: list

    :return: list of joints in hierarchical order
    """
    joints = []
    for i, loc in enumerate(locators):
        # Get position and name
        jnt_name = loc.replace(SUFFIX.LOCATOR, SUFFIX.JOINT)
        if name_modifier:
            split_name = jnt_name.split('_')
            start = '_'.join(split_name[:-1])
            print(split_name)
            print(start)
            print(split_name[-1])
            jnt_name = f'{start}_{name_modifier}_{split_name[-1]}'
        # Create joint at origin and with no parent
        jnt = cmds.joint(name=jnt_name)
        if cmds.listRelatives(jnt, parent=True):
            cmds.parent(jnt, world=True)
        # Parent to locator, zero out translation and joint orient, unparent
        cmds.parent(jnt, loc)
        cmds.xform(jnt, translation=(0, 0, 0))
        cmds.joint(name=jnt, edit=True, orientation=[0, 0, 0])
        cmds.parent(jnt, world=True)

        # Add joint to list
        joints.append(jnt)
        # Parent this joint to the previous one
        if i > 0:
            cmds.parent(joints[i], joints[i - 1])

    return joints

def create_fk_con(joint, con_name):
    """

    :param joint: joint to create control for
    :return:
    """
    control = cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), r=1.5, n=con_name)
    cmds.parent(control, joint)
    cmds.xform(control, translation=(0, 0, 0))
    cmds.select(joint)
    child = cmds.pickWalk(direction='down')
    cmds.parent(child, control)
    return control


def create_blend_chain(blend_jnts, fk_jnts, ik_jnts):
    """

    :param blend_jnts:
    :param fk_jnts:
    :param ik_jnts:
    :return:
    """
    # Create ik handle
    ik_root = ik_jnts[0]
    ik_end = ik_jnts[-1]
    cmds.ikHandle(solver='ikRPsolver', startJoint=ik_root, endEffector=ik_end)
    # Create fk controls
    for jnt in fk_jnts:
        if jnt != fk_jnts[-1]:
            con_name = jnt.replace(SUFFIX.JOINT, SUFFIX.CONTROL)
            create_fk_con(jnt, con_name)


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#