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

def enum(**enums):
    """
    Creates enums.
    """
    return type('Enum', (), enums)

#region enums

SUFFIX = enum(LOCATOR='LOC',
              JOINT='JNT',
              CURVE='CON')

SIDE = enum(R='R',
            L='L',
            C='C')

AXIS = enum(X='X',
            Y='Y',
            Z='Z')

#endregion enums