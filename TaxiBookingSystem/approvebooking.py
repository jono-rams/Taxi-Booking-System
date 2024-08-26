from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout,
                             QVBoxLayout, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from connection import Database


class ApproveBookingWidget(QWidget):
    @staticmethod
    def get_all_drivers():
        db = Database()
        db.connect("db/test.db")
        drivers_query = "SELECT name, driverID FROM driver WHERE status = 'Active'"
        drivers = db.execute_query(query=drivers_query)
        db.close_connection()
        return drivers or []

    def run_update(self):
        idx = self.driver_combobox.currentIndex()
        driver_id = self.drivers[idx][1]
        if driver_id:
            db = Database()
            db.connect("db/test.db")
            update_query = "UPDATE booking SET DriverID = ?, status = 'Confirmed' WHERE bookingID = ?"
            update_params = (driver_id, self.booking_id)
            db.insert_data(query=update_query, data=update_params)
            db.close_connection()
            QMessageBox.information(None, "Booking Updated", "Driver assigned successfully.")
            self.close()
        else:
            QMessageBox.warning(None, "Error", "Please select a driver.")

    def __init__(self, booking_id):
        super().__init__()

        self.booking_id = booking_id

        self.setWindowTitle("Assign Driver")
        self.setFixedSize(600, 400)

        # Create Vertical Layout
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        # Create Label Widget
        label = QLabel("Please Assign a Driver!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = QFont()
        font.setPointSize(18)
        font.setFamily("TimesNewRoman")
        label.setFont(font)
        label.setFixedHeight(30)

        v_layout.addWidget(label)

        # Create Horizontal Layout for Driver Combobox
        driver_layout = QHBoxLayout()
        driver_label = QLabel("Driver:")
        driver_layout.addWidget(driver_label)
        v_layout.addLayout(driver_layout)

        self.drivers = get_all_drivers()
        self.driver_combobox = QComboBox()
        driver_names = (driver[0] for driver in self.drivers)
        self.driver_combobox.addItems(driver_names)
        driver_layout.addWidget(self.driver_combobox)

        # Create Assign Button
        assign_btn = QPushButton("Assign")
        assign_btn.clicked.connect(self.run_update)
        v_layout.addWidget(assign_btn)
