from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QWidget, QHeaderView, QVBoxLayout, QTableView, QAbstractItemView
from PyQt6.QtCore import Qt, QTimer
from competition_ui import Ui_MainWindow

import sys

MAX_PLAYERS = 60
MAX_PLAYER_IN_GROUP = 6

class ScoreboardWindow(QWidget):
    def __init__(self, model):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableView()
        self.table.setModel(model)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle("Scoreboard")
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.Stretch)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.row = 0
        self.column = 0

    def scroll(self):
        index = self.table.model().index(self.row, self.column)
        self.table.scrollTo(index)
        self.row += 1
        if self.row > MAX_PLAYERS:
            self.row = 0

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setup_table()

        self.tableWidget.setSortingEnabled(True)
        self.actionClear.triggered.connect(self.clear)
        self.lineEdit.textChanged.connect(self.filter_table)
        self.tableWidget.itemChanged.connect(self._on_item_changed)
        self.actionScorebord.triggered.connect(self.show_scoreboard)

        self.clear()

        self.w = ScoreboardWindow(self.tableWidget.model())

        self.show()

    def setup_table(self):
        columns_labels = ["Group", "Number", "Name", "Lastname", "Class", "Club", "SKEET", "TRAP", "MOP", "Score"]
        self.tableWidget.setColumnCount(len(columns_labels))
        self.tableWidget.setHorizontalHeaderLabels(columns_labels)
        self.tableWidget.verticalHeader().setVisible(False)
    
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.Stretch)

    def show_scoreboard(self):
        if self.w.isHidden():
            self.w.show()
        else:
            self.w.hide()

    def _on_item_changed(self, item):
        self.tableWidget.blockSignals(True)
        row = item.row()
        skeet_score_item = self.tableWidget.item(row, 6)
        trap_score_item_item = self.tableWidget.item(row, 7)
        mop_score_item = self.tableWidget.item(row, 8)

        sum_value = 0

        if skeet_score_item and skeet_score_item.text().isdigit():
            sum_value += int(skeet_score_item.text())
        if trap_score_item_item and trap_score_item_item.text().isdigit():
            sum_value += int(trap_score_item_item.text())
        if mop_score_item and mop_score_item.text().isdigit():
            sum_value += int(mop_score_item.text())

        sum_item = QTableWidgetItem()
        sum_item.setData(Qt.ItemDataRole.DisplayRole, sum_value)
        self.tableWidget.setItem(row, 9, sum_item)
        self.tableWidget.blockSignals(False)

    def add_row(self):
        number_of_rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(number_of_rows)

        new_group_number_item =  QTableWidgetItem()
        new_group_number_item.setData(Qt.ItemDataRole.DisplayRole, number_of_rows//6+1)
        self.tableWidget.setItem(number_of_rows, 0, new_group_number_item)        

        new_start_number_item =  QTableWidgetItem()
        new_start_number_item.setData(Qt.ItemDataRole.DisplayRole, number_of_rows+1)
        self.tableWidget.setItem(number_of_rows, 1, new_start_number_item)

        new_item_skeet =  QTableWidgetItem()
        new_item_skeet.setData(Qt.ItemDataRole.DisplayRole, 0)         
        self.tableWidget.setItem(number_of_rows, 6, new_item_skeet)

        new_item_trap =  QTableWidgetItem()
        new_item_trap.setData(Qt.ItemDataRole.DisplayRole, 0)       
        self.tableWidget.setItem(number_of_rows, 7, new_item_trap)

        new_item_mop =  QTableWidgetItem()
        new_item_mop.setData(Qt.ItemDataRole.DisplayRole, 0)           
        self.tableWidget.setItem(number_of_rows, 8, new_item_mop)  

        new_item_final_score =  QTableWidgetItem()
        new_item_final_score.setData(Qt.ItemDataRole.DisplayRole, 0)           
        self.tableWidget.setItem(number_of_rows, 9, new_item_final_score)

    def remove_row(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())

    def clear(self):
        self.tableWidget.setRowCount(0)
        for _ in range(MAX_PLAYERS):
            self.add_row()

    def filter_table(self, filter_text):
        for row in range(self.tableWidget.rowCount()):
            match = False
            for col in range(self.tableWidget.colorCount()):
                item = self.tableWidget.item(row, col)
                if item is not None and filter_text.lower() in item.text().lower():
                    match = True
                    break
            self.tableWidget.setRowHidden(row, not match)
        

app = QApplication(sys.argv)
window = MainWindow()
timer = QTimer()
timer.timeout.connect(window.w.scroll)
timer.setInterval(500)
timer.start()
sys.exit(app.exec())