# Author: Thomas Lécluse
# Licence GPL-3

#
# Widget of editor frame
#

from PySide2.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QShortcut
from PySide2.QtGui import QColor, QTextFormat, QPainter, QSyntaxHighlighter, QTextCharFormat, QFont, QTextCursor, QKeySequence
from PySide2.QtCore import QRect, Slot, Qt, QSize, QRegExp

import re
from src.assets_manager import get_font

INDENT_SPACES = 2


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
        self.highlight = AssembleHighlighter(self.document(), config)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # default widget Signals binding
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Shortcuts
        shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_save.activated.connect(self.on_ctrl_s_activated)

        shortcut_open = QShortcut(QKeySequence("Ctrl+O"), self)
        shortcut_open.activated.connect(self.on_ctrl_o_activated)

        shortcut_indent_all = QShortcut(QKeySequence("Ctrl+T"), self)
        shortcut_indent_all.activated.connect(lambda: self.setPlainText(re_indent_all(self.toPlainText(), self.highlight.keywords)))

        # Change the font to get a fix size for characters
        doc = self.document()
        f = doc.defaultFont()
        f.setFamily(get_font(config))
        doc.setDefaultFont(f)

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

    def goto_line(self, line_nb):
        """
        Sets the cursor position at the end of the specified line
        :param line_nb: line number to go to
        """
        cursor = QTextCursor(self.document().findBlockByLineNumber(line_nb - 1))  # Line numbers starts at 0
        cursor.movePosition(QTextCursor.EndOfLine)
        self.setTextCursor(cursor)

    def on_ctrl_s_activated(self):
        pass

    def on_ctrl_o_activated(self):
        pass

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

    def keyPressEvent(self, e):
        super().keyPressEvent(e)

        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.auto_indent()

    def auto_indent(self):
        """
        Handles the indent operation
        """
        lines = self.toPlainText().split("\n")
        new_line_nb = self.textCursor().blockNumber()

        previous_line = lines[new_line_nb - 1]
        spaces = get_leading_space(previous_line)

        if leads_with_label(previous_line):
            spaces += INDENT_SPACES

        self.insertPlainText(" " * spaces)


class AssembleHighlighter(QSyntaxHighlighter):

    def __init__(self, document, config):
        """
        Handles the syntax highlighting for assemble language
        :param document: QPlaintTextEdit's document to format
        """
        QSyntaxHighlighter.__init__(self, document)

        self.styles = {
            'keyword': self.get_format(config.get('colors', 'asm_keywords')),
            'comment': self.get_format(config.get('colors', 'asm_comments')),
            'label': self.get_format(config.get('colors', 'asm_labels'), 'italic'),
            'directive': self.get_format(config.get('colors', 'asm_directives')),
            'numbers': self.get_format(config.get('colors', 'asm_numbers'), 'bold')
        }

        self.rules = []
        self.keywords = []
        self.init_rules([])  # Initialization with no keywords

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

    def init_rules(self, assemble_keywords):
        """
        Builds the language rules

        :param assemble_keywords: keywords of the language
        """
        self.keywords = assemble_keywords
        rules = []

        # Keywords
        rules += [(r'\b%s\b' % w, 0, self.styles['keyword']) for w in assemble_keywords]

        # Numeric literals
        rules += [
            (r'\b[0-9]+\b', 0, self.styles['numbers']),
            (r'\b0[xX][0-9A-Fa-f]+\b', 0, self.styles['numbers']),
            (r'\b0[bB][0-1]+\b', 0, self.styles['numbers'])
        ]

        # Comments
        rules += [
            (r'//[^\n]*', 0, self.styles['comment'])
        ]

        # Labels
        rules += [
            (r'(^\s*:\w+)', 0, self.styles['label'])
        ]

        # Directives
        rules += [
            (r'(^\s*%define\b|^\s*%data\b)', 0, self.styles['directive'])
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


#
# Indent feature methods
#

def get_leading_space(text):
    """
    Gets the number of leading whitespaces of the previous line
    :param text: text to analyze
    :return: number of leading blank spaces
    :rtype: int
    """
    return [(m.start(), m.end() - m.start()) for m in re.finditer(r'^\s*', text)][0][1]


def leads_with_label(text):
    """
    Checks if the specified texts starts with a leading label.

    :param text: text to analyze
    :return: True if a label leads the line
    :rtype: bool
    """
    return len([(m.start(), m.end() - m.start()) for m in re.finditer(r'(^\s*:\w+)', text)]) > 0


def leads_with_directive(text):
    """
    Checks if the specified texts starts with a leading directive.

    :param text: text to analyze
    :return: True if a directive leads the line
    :rtype: bool
    """
    return len([(m.start(), m.end() - m.start()) for m in re.finditer(r'(^\s*%\w+)', text)]) > 0


def re_indent_all(text, keywords):
    """
    Re-format the given text line by line with the following rules:
    - 2 spaces before instruction
    - 1 tab after instruction
    - Labels are at the beginning of the line

    :param text: text to indent
    :param keywords: list of the languages keywords (instructions
    :return: indent text
    :rtype: str
    """
    res = ""
    previous_indent = 0

    for line in text.split("\n"):
        new_line = ""

        words = line.replace("\t", " ").split()  # Replace all the tabs by spaces so that we can reprocess all the indent

        # Check for comments
        comment = ""
        if '//' in words:
            comment_index = words.index('//')
            comment = __build_comment(words[comment_index:])

            words = words[:comment_index]

        # Check for labels
        if leads_with_label(line):
            new_line += words[0] + " "  # Label has to be the first element
            previous_indent = INDENT_SPACES  # Reset the indent level
        else:
            # Reset indentation for directives or after 2 blank lines (which makes 3*'\n' because there is a newline before)
            if leads_with_directive(line) or (len(res) > 2 and res[::-1].replace(" ", "").startswith("\n"*3)):
                previous_indent = 0

            # If there is no words left after parsing the comment, it means the the line was a comment.
            # In that case, we do not indent the line-comment
            if len(words) != 0:
                # Start by adding the indent
                new_line += " " * previous_indent

            for w in words:
                if w in keywords:
                    new_line += w + "\t"  # Add tab after keyword
                else:
                    new_line += w + " "

        new_line += comment + "\n"
        res += new_line

    return res


def __build_comment(list_words):
    """
    Creates a string comment by separating all words with a blank space

    :param list_words: all words to concatenate
    :rtype: str
    """
    comment = ""
    for w in list_words:
        comment += w + " "

    return comment
