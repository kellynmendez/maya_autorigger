#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kellyn Mendez

:synopsis:
    This module contains general python utilities
"""


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in
import xml.etree.ElementTree as ElementTree
import os

# Third party
import maya.cmds as cmds

# Internal

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#


def _read_xml_helper(xml_nodes):
    """
    Reads an XML file and stores its data as a dictionary.

    :param xml_nodes: The top level ElementTree xml nodes
    :return: str
    """
    if len(xml_nodes):
        xml_dict = Autovivification()
        for node in xml_nodes:
            dict_name = node.tag
            block_data = list(node)

            # Recurse until no children are left.
            if block_data:
                xml_dict[dict_name] = _read_xml_helper(xml_nodes=block_data)
            else:
                # When no children exist, get the value and load the value.
                xml_dict[dict_name] = node.attrib['value']
        return xml_dict

    return None


def read_xml(xml_path):
    """

    :param xml_path:
    :return:
    """
    # Does the path exist.
    if not os.path.isfile(xml_path):
        cmds.warning('The file is not valid')
        return False

    # Check for contents.
    xml_fh = ElementTree.parse(xml_path, parser=ElementTree.XMLParser(encoding="utf-8"))
    root = xml_fh.getroot()
    if not list(root):
        cmds.warning(f"No data found in {xml_path}")
        return None

    xml_dict = _read_xml_helper(root)

    return xml_dict

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Autovivification(dict):
    """
    This is a Python implementation of Perl's Autovivification feature.
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value