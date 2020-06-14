# Author: Thomas Lécluse
# License GPL-3

#
# About-us frame
#

from PySide2.QtWidgets import QVBoxLayout, QLabel, QWidget
from PySide2.QtGui import QPixmap, Qt
from PySide2.QtCore import QSize


from src.view.style import style

class AboutFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config):
        """
        About-us frame.
        """
        QWidget.__init__(self)

        self.config = config

        self.setWindowTitle("DigiQt - About us")

        self.links_style = '<style>a { text-decoration:none; color:cyan; } </style>'
        self.contact_style = '<style>a { text-decoration:none; color:lightblue; } </style>'

        self._set_layout()
        self.setStyleSheet(style.get_stylesheet("aboutbox"))

    def _set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addSpacing(20)
        AboutLabel("Made by\nOlivier Lécluse & Thomas Lécluse", box)

        logo = QLabel()
        logo.setPixmap(QPixmap("assets/LDC-light"))
        logo.setFixedSize(QSize(512, 222))  # Original dimension is 2048x888, we divided by 4
        logo.setScaledContents(True)
        box.addWidget(logo)
        box.setAlignment(logo, Qt.AlignCenter)

        AboutLabel(
            f'{self.links_style}<a href="https://bradsprojects.com/digirule2/">&gt; Digirule2 project &lt;</a>', box, True)

        AboutLabel(
            f'{self.links_style}<a href="https://github.com/wawachief/DigiQt">&gt; GitHub project &lt;</a>', box, True)

        AboutLabel(
            f'Contact: {self.contact_style}<a href="mailto:devcorp@lecluse.fr">devcorp@lecluse.fr</a>', box, True)

        AboutLabel(f"Version: {self.config.get('main', 'APP_VERSION')}", box)

        box.addSpacing(20)

        self.setLayout(box)

    # --- Close handler ---

    def closeEvent(self, event):
        """
        Event called upon a red-cross click.
        """
        self.on_close()

    def on_close(self):
        """
        Reroot this method in the Main Frame in order to Updates the execution frame's open editor icon and tooltip
        :return:
        """
        pass


class AboutLabel(QLabel):
    def __init__(self, text, layout, clickable=False):
        """
        Custom labels for about box
        """
        QLabel.__init__(self, text)

        self.setOpenExternalLinks(clickable)
        self.setAlignment(Qt.AlignCenter)

        layout.addWidget(self)
        layout.setAlignment(self, Qt.AlignCenter)
