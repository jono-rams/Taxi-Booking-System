import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt
import datetime
from connection import Database
from booking import BookingWidget


class ViewBookings(QWidget):
    def handle_close(self):
        self.close()
        self.dash_reference.show()

    def __init__(self, driver_id, dash_reference):
        super().__init__()

        self.driver_id = driver_id
        self.booking_widget = None
        self.dash_reference = dash_reference

        self.setWindowTitle("All Bookings")
        self.setFixedSize(800, 450)
        self.layout = QVBoxLayout(self)

        # Scroll Area to hold the content
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area)

        self.db = Database()
        self.db.connect("db/test.db")
        booking_query = "SELECT * FROM booking WHERE DriverID = ? AND PickupDate >= ?"
        today = datetime.date.today()
        booking_params = (self.driver_id, today)
        self.bookings = self.db.execute_query(query=booking_query, params=booking_params, fetch_all=True)
        self.db.close_connection()

        # Add an entry for each booking
        for i in range(len(self.bookings)):
            entry_layout = QHBoxLayout()
            label = QLabel(f"Booking {i}")
            entry_layout.addWidget(label)

            view_btn = QPushButton("View")
            view_btn.setFixedSize(120, 50)
            view_btn.clicked.connect(lambda index=i: self.handle_view_click(index=index))
            entry_layout.addWidget(view_btn)

            scroll_layout.addLayout(entry_layout)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Add close button
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedSize(100, 50)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def handle_view_click(self, index):
        # Call view booking data with index to pull data from bookings
        self.booking_widget = BookingWidget(booking=self.bookings[index])
        self.booking_widget.show()
