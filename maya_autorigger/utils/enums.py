#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez

:synopsis:
    This module contains all enums for rigging.
"""

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------- ENUMS --#

def enum(**enums):
    """
    Creates enums.
    """
    return type('Enum', (), enums)

#region enums

SUFFIX = enum(LOCATOR='LOC',
              JOINT='JNT',
              CONTROL='CON')

SIDE = enum(R='R',
            L='L',
            C='C')

AXIS = enum(X=(1, 0, 0),
            Y=(0, 1, 0),
            Z=(0, 0, 1))

JNT_NAME = enum(ARM='arm',
            SHOULDER='shoulder',
            UPPERARM='upperArm',
            ELBOW='elbow',
            FOREARM='forearm',
            WRIST='wrist',
            HAND='hand',
            FINGER='finger')

TEMPLATE_KEY = enum(COMPONENT='component',
                    INFO='info',
                    CHILDREN='children',
                    MODULE='module',
                    NUM_COMPS='num_comps',
                    SIDE="side",
                    AXIS="axis",
                    START_POS="start_pos",
                    NUM_JOINTS="num_joints")

DEFAULT_LENGTH = enum(Arm=36.0,
                      Finger=6.0,
                      Spacer=10.0)

#endregion enums