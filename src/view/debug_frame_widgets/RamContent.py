# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of debug frame
#

from PySide2.QtWidgets import QPlainTextEdit
from PySide2.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat, QFont, QPalette, QTextCursor
from PySide2.QtCore import QRegExp

from src.assets_manager import get_font

class RamDebugText(QPlainTextEdit):

    def __init__(self, config, parent=None):
        """
        Holds the content of the RAM (for debug purposes)

        :param config: configuration file
        """
        QPlainTextEdit.__init__(self, parent)

        self.config = config
        self.setReadOnly(True)
        self.highlight = RamHighlighter(self.document(), config)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.sig_rampc_goto = None  # attribute pushed by debugger controler

        # Change the font to get a fix size for characters
        doc = self.document()
        f = doc.defaultFont()
        f.setFamily(get_font(config))
        doc.setDefaultFont(f)

    def select(self, row, column, color):
        """
        Highlights the given position
        """
        cursor = self.textCursor()

        cursor.setPosition(0)  # Move to the beggining
        cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, row)  # Move to the row
        cursor.movePosition(QTextCursor.WordRight, QTextCursor.MoveAnchor, column + 2)  # Move to the column

        cursor.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor, 1)  # Select the color
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)  # un-select blank space

        self.setTextCursor(cursor)

        p = self.palette()
        p.setColor(QPalette.Highlight, QColor(self.config.get('colors', color)))
        p.setColor(QPalette.HighlightedText, QColor('black'))
        self.setPalette(p)

    def mouseDoubleClickEvent(self, e):
        """
        Overrides the keyPress event in order to not write anything
        """
        super().mouseDoubleClickEvent(e)

        cursor = self.textCursor()

        row = cursor.blockNumber()
        y = cursor.columnNumber()

        line = cursor.block().text()
        col = 0
        began = False
        for i in range(y):
            if line[i] == ':':
                began = True
            elif began and line[i] == " ":
                col += 1

        col -= 2  # to remove beginning spaces counts

        if col >= 0:  # to be sure that we click on a valid position
            # print(row, col)  # TODO link to signal
            self.sig_rampc_goto.emit(f"{row} {col}")
        else:
            cursor.clearSelection()
            self.setTextCursor(cursor)


class RamHighlighter(QSyntaxHighlighter):

    def __init__(self, document, config):
        """
        Handles the highlighting of the identified elements
        :param document: QPlaintTextEdit's document to format
        """
        QSyntaxHighlighter.__init__(self, document)

        self.styles = {
            'label': self.get_format(config.get('colors', 'asm_labels'), 'italic'),
        }

        self.rules = []
        self.init_rules()

    # --- Coloration ---
    def get_format(self, color, style=''):
        """
        Returns a QTextCharFormat with the given attributes
        :param color:
        :param style:
        :return:
        """
        c = QColor()
        c.setNamedColor(color)

        f = QTextCharFormat()
        f.setForeground(c)

        if 'bold' in style:
            f.setFontWeight(QFont.Bold)

        if 'italic' in style:
            f.setFontItalic(True)

        return f

    def init_rules(self):
        """
        Builds the formatting rules
        """
        rules = []

        # Labels
        rules += [
            (r'(^[0-9a-fA-F]+:)', 0, self.styles['label'])
        ]

        # Build QRegExp for the above patterns
        self.rules = [(QRegExp(pattern), index, f) for (pattern, index, f) in rules]

        # Update all
        self.rehighlight()

    def highlightBlock(self, text):
        """
        Performs the highlight operation
        :param text: text to format
        """
        # For each rules...
        for expression, nth, f in self.rules:
            # ...we look for matches
            index = expression.indexIn(text.lower(), 0)
            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, f)  # Format and color the text
                index = expression.indexIn(text.lower(), index + length)  # update index for next iteration

        self.setCurrentBlockState(0)
