# Author: Thomas Lécluse
# License GPL-3

#
# Symbols and labels frame
#

from PySide2.QtWidgets import QWidget, QListView, QGridLayout, QAbstractItemView, QLabel
from PySide2.QtCore import QSize, QItemSelection, QModelIndex, Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem

from src.view.style import style


class SymbolViewFrame(QWidget):

    # --- Init methods ---

    def __init__(self, config):
        """
        Symbols and Labels view frame

        :param config: application configuration file
        """
        QWidget.__init__(self)

        self.setFixedSize(QSize(220, 330))
        self.setWindowTitle("DigiQt - Symbols")

        self.config = config

        self.lab_label = QLabel("Labels")
        self.lab_label.setAlignment(Qt.AlignCenter)
        self.lab_symbols = QLabel("Symbols")
        self.lab_symbols.setAlignment(Qt.AlignCenter)

        self.sig_symbol_goto = None # pushed by the controler

        # Initialization of the lists
        self.labels_view = QListView()
        self.labels_view.setFixedSize(QSize(100, 300))
        self.labels_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.labels_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dm_labels = QStandardItemModel(self.labels_view)

        self.symbols_view = QListView()
        self.symbols_view.setFixedSize(QSize(100, 300))
        self.symbols_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.symbols_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dm_symbols = QStandardItemModel(self.symbols_view)

        self.init_labels([])
        self.init_symbols([])

        self.labels_view.clicked.connect(self.on_label_changed)
        self.symbols_view.clicked.connect(self.on_symbol_changed)

        self.__set_layout()
        self.setStyleSheet(style.get_stylesheet("listviews_frame"))

    def init_labels(self, list_labels):
        """
        Initiates the data model for the labels

        :param list_labels: list of labels
        """
        self.__init_view(self.labels_view, self.dm_labels, list_labels)

    def init_symbols(self, list_symbols):
        """
        Initiates the data model for the symbols

        :param list_symbols: list of symbols
        """
        self.__init_view(self.symbols_view, self.dm_symbols, list_symbols)

    def __init_view(self, list_view, data_model, objects_list):
        """
        Initiates the view given the data_model and the objects to add in it.

        :type list_view: QListView
        :type data_model: QStandardItemModel
        :type objects_list: list
        """
        data_model.clear()

        for l in objects_list:
            data_model.appendRow(QStandardItem(l))

        list_view.setModel(data_model)

    def __set_layout(self):
        """
        Creates this Widget's Layout
        """
        box = QGridLayout()
        box.setContentsMargins(0, 0, 0, 0)

        box.addWidget(self.lab_label, 0, 0)
        box.addWidget(self.labels_view, 1, 0)
        box.addWidget(self.lab_symbols, 0, 1)
        box.addWidget(self.symbols_view, 1, 1)

        self.setLayout(box)

    def on_label_changed(self, item):
        """
        Callback method for the label change signal

        :param item: new item selected
        :type item: QItemSelection
        """
        text = item.data()
        if text:
            self.sig_symbol_goto.emit(text)

    def on_symbol_changed(self, item):
        """
        Callback method for the symbol change signal
        :param item: new item selected
        :type item: QItemSelection
        """
        text = item.data()
        if text:
            self.sig_symbol_goto.emit(text)

    def __retrieve_text(self, data_model, item):
        """
        Gets the text with the specified data model from a QItemSelection

        :type item: QItemSelection
        :type data_model: QStandardItemModel
        :rtype: str
        """
        selection = item.indexes()
        if selection:
            return data_model.item(QModelIndex(selection[0]).row()).text()

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
