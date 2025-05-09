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
import os

# Third party
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

from maya_autorigger.biped import Biped


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

        self.num_arm_jnts_box = None
        self.locators_created = False

        self.biped = None

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
        self.num_arm_jnts_box = QtWidgets.QSpinBox()
        self.num_arm_jnts_box.setFixedWidth(100)
        self.num_arm_jnts_box.setValue(3)
        self.num_arm_jnts_box.setSingleStep(2)
        self.num_arm_jnts_box.setMinimum(3)
        arm_jnt_num_row.addWidget(self.num_arm_jnts_box)
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
        if self.num_arm_jnts_box.value() < 3 or self.num_arm_jnts_box.value() % 2 == 0:
            self.warn_user(title="Error",
                           msg="Number of arm joints must be an even number and greater "
                               "than or equal to 3.       ")
            return None
        self.biped = Biped(arm_jnt_num=self.num_arm_jnts_box.value(), template_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates\\arm.xml"))
        self.biped.create_locators()
        self.locators_created = True
        return True


    def generate_joints(self):
        """

        :return:
        """
        if not self.locators_created:
            self.warn_user(title="Error",
                           msg="Locators must be created before generating "
                               "joints.       ")
            return None
        self.biped.create_joints()
        return True


    @classmethod
    def warn_user(cls, title=None, msg=None):
        """
        This function displays a message box that locks the screen until the user
        acknowledges it.

        :param title: The title of the message box window.
        :type: str

        :param msg: The text to show in the message box window.
        :type: str
        """
        if msg and title:
            # Create a QMessageBox
            msg_box = QtWidgets.QMessageBox()
            # Set the title and the message of the window
            msg_box.setWindowTitle(title)
            msg_box.setText(msg)
            # Show the message
            msg_box.exec_()