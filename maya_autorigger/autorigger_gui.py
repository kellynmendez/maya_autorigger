#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez

:synopsis:
    This module contains utilities for working with guis in maya.
"""


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in

# Third party
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

# Internal

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def get_maya_window():
    """
    This gets a reference to the Maya window.

    :return: A reference to the Maya window.
    :type: QtGui.QtDialog
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class AutoRiggerGUI(QtWidgets.QDialog):
    """
    Displays the GUI to automate playblasting a turntable
    """
    def __init__(self):
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        """
        Creates and displays the GUI to the user
        """
        main_vb = QtWidgets.QVBoxLayout(self)
        components_lay = QtWidgets.QFormLayout()

        # Create the arm joint number row
        arm_jnt_num_row = QtWidgets.QHBoxLayout()
        # Arm joint num label
        arm_jnt_num_lbl = QtWidgets.QLabel('Number of Arm Joints: ')
        arm_jnt_num_row.addWidget(arm_jnt_num_lbl)
        # Arm joint num spin box
        arm_jnt_num_sb = QtWidgets.QSpinBox()
        arm_jnt_num_sb.setFixedWidth(100)
        arm_jnt_num_sb.setValue(3)
        arm_jnt_num_sb.setSingleStep(2)
        arm_jnt_num_row.addWidget(arm_jnt_num_sb)
        # Add to component layout
        components_lay.addRow(arm_jnt_num_row)

        # Add components to main layout
        main_vb.addLayout(components_lay)

        # Make create locators button
        create_loc_btn = QtWidgets.QPushButton('Create Locators')
        create_loc_btn.clicked.connect(self.create_locators)
        create_loc_btn.setStyleSheet('background-color:violet')
        main_vb.addWidget(create_loc_btn)
        # Make generate joints button
        gen_jnts_btn = QtWidgets.QPushButton('Generate Joints')
        gen_jnts_btn.clicked.connect(self.generate_joints)
        gen_jnts_btn.setStyleSheet('background-color:forestgreen')
        main_vb.addWidget(gen_jnts_btn)

        # Add title to window
        self.setWindowTitle('Arm Auto Rigger')
        # Show the GUI to the user
        self.setGeometry(350, 350, 200, 150)
        self.show()

    def create_locators(self):
        """

        :return:
        """

    def generate_joints(self):
        """

        :return:
        """