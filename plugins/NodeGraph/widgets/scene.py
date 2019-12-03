# -*- coding: utf-8 -*-
"""

Script Name: scene.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from appData import (VIEWER_BG_COLOR, VIEWER_GRID_SIZE, VIEWER_GRID_OVERLAY, VIEWER_GRID_COLOR)

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QColor, QPen, QPainterPath, QPainter

class NodeScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(NodeScene, self).__init__(parent)
        self.background_color = VIEWER_BG_COLOR
        self.grid = VIEWER_GRID_OVERLAY
        self.grid_color = VIEWER_GRID_COLOR

    def __repr__(self):
        return '{}.{}(\'{}\')'.format(self.__module__,
                                      self.__class__.__name__,
                                      self.viewer())

    def _draw_grid(self, painter, rect, pen, grid_size):
        lines = []
        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)
        x = left
        while x < rect.right():
            x += grid_size
            lines.append(QLineF(x, rect.top(), x, rect.bottom()))
        y = top
        while y < rect.bottom():
            y += grid_size
            lines.append(QLineF(rect.left(), y, rect.right(), y))
        painter.setPen(pen)
        painter.drawLines(lines)

    def drawBackground(self, painter, rect):
        painter.save()

        bg_color = QColor(*self._bg_color)
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setBrush(bg_color)
        painter.drawRect(rect)

        if not self._grid:
            painter.restore()
            return

        zoom = self.viewer().get_zoom()

        if zoom > -0.5:
            pen = QPen(QColor(*self.grid_color), 0.65)
            self._draw_grid(painter, rect, pen, VIEWER_GRID_SIZE)

        color = bg_color.darker(150)
        if zoom < -0.0:
            color = color.darker(100 - int(zoom * 110))
        pen = QPen(color, 0.65)
        self._draw_grid(painter, rect, pen, VIEWER_GRID_SIZE * 8)

        # fix border issue on the scene edge.
        pen = QPen(bg_color, 2)
        pen.setCosmetic(True)
        path = QPainterPath()
        path.addRect(rect)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.restore()

    def mousePressEvent(self, event):
        selected_nodes = self.viewer().selected_nodes()
        if self.viewer():
            self.viewer().sceneMousePressEvent(event)
        super(NodeScene, self).mousePressEvent(event)
        keep_selection = any([
            event.button() == Qt.MiddleButton,
            event.button() == Qt.RightButton,
            event.modifiers() == Qt.AltModifier
        ])
        if keep_selection:
            for node in selected_nodes:
                node.setSelected(True)

    def mouseMoveEvent(self, event):
        if self.viewer():
            self.viewer().sceneMouseMoveEvent(event)
        super(NodeScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.viewer():
            self.viewer().sceneMouseReleaseEvent(event)
        super(NodeScene, self).mouseReleaseEvent(event)

    def viewer(self):
        return self.views()[0] if self.views() else None

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, mode=True):
        self._grid = mode

    @property
    def grid_color(self):
        return self._grid_color

    @grid_color.setter
    def grid_color(self, color=(0, 0, 0)):
        self._grid_color = color

    @property
    def background_color(self):
        return self._bg_color

    @background_color.setter
    def background_color(self, color=(0, 0, 0)):
        self._bg_color = color


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 2:06 AM
# © 2017 - 2018 DAMGteam. All rights reserved