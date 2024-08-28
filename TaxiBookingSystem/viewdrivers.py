from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QTableWidget, QPushButton, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from driverviewbookings import ViewBookings
from connection import Database


# Window class to display all drivers in a scrollable list
class AllDriversWindow(QWidget):
    def fetch_all_drivers(self):
        db = Database()
        db.connect(self.db_path)
        fetch_query = "SELECT DriverID, Name, PlateNo, Status, LicenseExpiry FROM Driver"
        drivers = db.execute_query(fetch_query, fetch_all=True)
        db.close_connection()

        return drivers or []

    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle("All Drivers")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #333; color: white;")

        layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        drivers = self.fetch_all_drivers()
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(drivers))
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Driver ID", "Name", "Plate No", "Status", "License Exp"])

        for row_idx, driver in enumerate(drivers):
            for col_idx, item in enumerate(driver):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

        self.table_widget.cellDoubleClicked.connect(self.openDriverBookings)
        scroll_layout.addWidget(self.table_widget)

        btn_edit = QPushButton("Edit")
        btn_edit.setFont(QFont('Helvetica', 10))
        btn_edit.setStyleSheet("background-color: #000000; padding: 10px; color: yellow;")
        btn_edit.clicked.connect(self.enableEditing)
        scroll_layout.addWidget(btn_edit)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        scroll_layout.addWidget(close_btn)

    def enableEditing(self):
        for row in range(self.table_widget.rowCount()):
            self.table_widget.item(row, 3).setFlags(self.table_widget.item(row, 3).flags() | Qt.ItemFlag.ItemIsEditable)
            self.table_widget.item(row, 3).setForeground(Qt.GlobalColor.black)

    def openDriverBookings(self, row, column):
        if column == 0:  # Assuming Driver ID is in the first column
            driver_id = int(self.table_widget.item(row, column).text())
            self.driver_bookings = ViewBookings(driver_id=driver_id, db_path=self.db_path, dash_reference=self, is_admin=True)
            self.driver_bookings.show()
