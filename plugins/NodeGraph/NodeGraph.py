# -*- coding: utf-8 -*-
"""

Script Name: NodeGraph.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os
import sys

from plugins.NodeGraph import (NodeGraph, BaseNode, BackdropNode, setup_context_menu,  QtCore,
                               PropertiesBinWidget, NodeTreeWidget)

from plugins.NodeGraph.assets import basic_nodes, widget_nodes


class MyNode(BaseNode):

    __identifier__ = 'com.chantasticvfx'
    NODE_NAME = 'my node'

    def __init__(self):
        super(MyNode, self).__init__()
        self.set_color(25, 58, 51)

        self.add_input('in port', color=(200, 10, 0))
        self.add_output('out port')


graph = NodeGraph()
setup_context_menu(graph)
viewer = graph.viewer()
viewer.show()

properties_bin = PropertiesBinWidget(node_graph=graph)
properties_bin.setWindowFlags(QtCore.Qt.Tool)
def show_prop_bin(node):
    if not properties_bin.isVisible():
        properties_bin.show()
graph.node_double_clicked.connect(show_prop_bin)

node_tree = NodeTreeWidget(node_graph=graph)
def show_nodes_list(node):
    if not node_tree.isVisible():
        node_tree.update()
        node_tree.show()
graph.node_double_clicked.connect(show_nodes_list)

reg_nodes = [
    BackdropNode, MyNode,
    basic_nodes.FooNode,
    basic_nodes.BarNode,
    widget_nodes.DropdownMenuNode,
    widget_nodes.TextInputNode,
    widget_nodes.CheckboxNode
]
for n in reg_nodes:
    graph.register_node(n)

my_node = graph.create_node('com.chantasticvfx.MyNode',
                            name='chantastic!',
                            color='#0a1e20',
                            text_color='#feab20',
                            pos=[310, 10])

foo_node = graph.create_node('com.chantasticvfx.FooNode',
                             name='node',
                             pos=[-480, 140])
foo_node.set_disabled(True)

# create example "TextInputNode".
text_node = graph.create_node('com.chantasticvfx.TextInputNode',
                              name='text node',
                              pos=[-480, -160])

# create example "TextInputNode".
checkbox_node = graph.create_node('com.chantasticvfx.CheckboxNode',
                              name='checkbox node',
                              pos=[-480, -20])

# create node with a combo box menu.
menu_node = graph.create_node('com.chantasticvfx.DropdownMenuNode',
                              name='menu node',
                              pos=[280, -200])

# change node icon.
this_path = os.path.dirname(os.path.abspath(__file__))
icon = os.path.join(this_path, 'assets', 'pear.png')
bar_node = graph.create_node('com.chantasticvfx.BarNode')
bar_node.set_icon(icon)
bar_node.set_name('icon node')
bar_node.set_pos(-70, 10)

# connect the nodes
foo_node.set_output(0, bar_node.input(2))
menu_node.set_input(0, bar_node.output(1))
bar_node.set_input(0, text_node.output(0))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/12/2019 - 11:36 PM
# © 2017 - 2018 DAMGteam. All rights reserved