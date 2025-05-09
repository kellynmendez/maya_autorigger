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
import re

# Third party
import maya.cmds as cmds

# Internal
from maya_autorigger.utils.enums import SUFFIX, JNT_NAME


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
    cmds.select(clear=True)
    for i, loc in enumerate(locators):
        # Get position and name
        jnt_name = loc.replace(SUFFIX.LOCATOR, SUFFIX.JOINT)
        if name_modifier:
            split_name = jnt_name.split('_')
            start = '_'.join(split_name[:-1])
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

def create_cube_con(name):
    """
    Creates a box curve

    :param name: The name of the curve
    :type: str

    :return: The curve
    """
    box_con = cmds.curve(degree=1, point=[(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1), (0, 0, 0),
                                     (0, 1, 0), (1, 1, 0), (1, 0, 0), (1, 1, 0),
                                     (1, 1, 1), (1, 0, 1), (1, 1, 1),
                                     (0, 1, 1), (0, 0, 1), (0, 1, 1), (0, 1, 0)])

    cmds.CenterPivot()
    cmds.xform(box_con, translation=(-.5, -.5, -.5))
    cmds.select(box_con)
    cmds.FreezeTransformations()
    cmds.rename(name)
    cmds.delete(constructionHistory=1)
    cmds.select(clear=True)

    return box_con

def create_con_on_jnt(joint, control):
    """

    :param control:
    :param joint: joint to create control for
    :return:
    """
    cmds.parent(control, joint)
    cmds.xform(control, translation=(0, 0, 0))
    child = cmds.pickWalk(joint, direction='down')
    cmds.parent(child, control)


def create_arm_blend_chain(blend_jnts, fk_jnts, ik_jnts):
    """

    :param blend_jnts:
    :param fk_jnts:
    :param ik_jnts:
    :return:
    """
    # Create fk controls
    for jnt in fk_jnts:
        if jnt != fk_jnts[-1]:
            con_name = jnt.replace(SUFFIX.JOINT, SUFFIX.CONTROL)
            control = cmds.circle(nr=(1, 0, 0), c=(0, 0, 0), r=1.5, n=con_name)
            create_con_on_jnt(jnt, control)

    # Create ik controls
    ik_root = ik_jnts[0]
    ik_end = ik_jnts[-1]
    blend_end = blend_jnts[-1]
    ik_con_name = ik_root.replace(SUFFIX.JOINT, SUFFIX.CONTROL)
    ik_handle = cmds.ikHandle(solver='ikRPsolver', startJoint=ik_root, endEffector=ik_end)
    ik_con = cmds.curve(point=[(0, 0, -1), (0, 1, 0), (0, 0, 1), (0, -1, 0), (0, 0, -1)],
                        degree=1, name=ik_con_name)
    print(ik_handle)
    print(ik_con)
    cmds.parent(ik_con, ik_handle[0])
    cmds.xform(ik_con, translation=(0, 0, 0))
    cmds.parent(ik_con, world=True)
    cmds.parent(ik_handle[0], ik_con)

    # Create hand control
    blend_end = blend_jnts[-1]
    side = blend_end.split('_')[0]
    hand_con = f'{side}_{JNT_NAME.HAND}_{SUFFIX.CONTROL}'
    create_cube_con(hand_con)
    cmds.parent(hand_con, blend_end)
    cmds.xform(hand_con, translation=(0, 0, 0))

    # Blend them
    cmds.addAttr(hand_con, longName='ikFkSwitch', attributeType='float',
                 minValue=0, maxValue=1)
    fk_ik_attr = hand_con + '.ikFkSwitch'
    cmds.setAttr(fk_ik_attr, edit=True, keyable=True)

    for blend in blend_jnts[:-1]:
        # Create blend colors node
        blend_colors = cmds.createNode('blendColors', name=blend + '_BC')
        # Connect rotate values from ik and fk joints to blend colors
        print(blend)
        fk = blend.replace('blend', 'fk')
        ik = blend.replace('blend', 'ik')
        cmds.connectAttr((ik + '.rotate'), (blend_colors + '.color1'), force=True)
        cmds.connectAttr((fk + '.rotate'), (blend_colors + '.color2'), force=True)

        # Connect blend colors output to the blend joint's rotate
        cmds.connectAttr((blend_colors + '.output'), (blend + '.rotate'), force=True)
        # Connect the fk ik switch attribute to the blender
        cmds.connectAttr(fk_ik_attr, (blend_colors + '.blender'), force=True)

        # Set the visibility
        reverse = cmds.createNode('reverse', name=hand_con + '_REV')
        cmds.connectAttr(fk_ik_attr, (reverse + '.inputX'), force=True)
        cmds.connectAttr((reverse + '.outputX'), (fk + '.visibility'), force=True)
        cmds.connectAttr(fk_ik_attr, (ik + '.visibility'), force=True)

    arm_grp_name = f'{side}_{JNT_NAME.ARM}_{SUFFIX.GROUP}'
    cmds.group(blend_jnts[0], ik_jnts[0], fk_jnts[0], n=arm_grp_name)

    cmds.select(clear=True)


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#