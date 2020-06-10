# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of editor frame
#

from PySide2.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PySide2.QtGui import QColor, QTextFormat, QPainter
from PySide2.QtCore import QRect, Slot, Qt, QSize


class LineNumberArea(QWidget):
    def __init__(self, editor):
        """
        Line number widget, handles the painting of the line numbers next to the edition widget
        """
        QWidget.__init__(self, parent=editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.get_line_number_area_width(), 0)

    def paintEvent(self, event):
        self.codeEditor.line_number_area_paint(event)


class CodeEditor(QPlainTextEdit):

    def __init__(self, config, parent=None):
        """
        Code editor widget

        :param config: configuration file
        :param parent:
        """
        QPlainTextEdit.__init__(self, parent)

        self.config = config
        self.line_number_area = LineNumberArea(self)

        # default widget Signals binding
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # initialization
        self.blockCountChanged.emit(0)
        self.cursorPositionChanged.emit()

    def line_number_area_paint(self, event):
        """
        Paints the line numbers next to the code editor
        """
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(self.config.get('colors', 'editor_lines_area_bg')))
        painter.setPen(QColor(self.config.get('colors', 'editor_lines_area_text')))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.line_number_area.width(),
                                 self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def get_line_number_area_width(self):
        """
        :return: width to use for the lines area (calculated with the number of lines digits)
        """
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.get_line_number_area_width(), cr.height()))

    @Slot(int)
    def update_line_number_area_width(self, new_bock_count):
        """
        Updates the width of the line numbers area
        """
        self.setViewportMargins(self.get_line_number_area_width(), 0, 0, 0)

    @Slot()
    def highlight_current_line(self):
        """
        Highlights the current edited line
        """
        line_selection = []

        if not self.isReadOnly():

            # Selection formatting
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(self.config.get('colors', 'editor_current_line_bg'))
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            line_selection.append(selection)

        self.setExtraSelections(line_selection)

    @Slot(QRect, int)
    def update_line_number_area(self, rect, dy):
        """
        Updates the displayed viewport of the line numbers area
        """
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.blockCountChanged.emit(0)
