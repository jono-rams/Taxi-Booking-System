from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPalette, QColor
from connection import Database
from bookingdetails import BookingWidget
import datetime


# Window class to display all upcoming bookings in a scrollable list
class UpcomingBookings(QWidget):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.db = Database()
        self.bookings = None
        self.booking_widget = None
        self.initUI()

    def initUI(self):
        # Set up the All Bookings window
        self.setWindowTitle("My Upcoming Bookings")
        self.setGeometry(100, 100, 600, 400)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(160, 185, 185))  # Applies background color to dashboard
        self.setPalette(palette)  # Set colors and style

        # Create a vertical layout for the scroll area and the scroll widget
        layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidgetResizable(True)  # Automatically resizes widget
        scroll_area.setWidget(scroll_widget)  # Scroll allows maneuvering of content if it does not fit in visible area
        layout.addWidget(scroll_area)

        # Load bookings and create buttons to view each booking's details
        self.db.connect(self.db_path)
        booking_query = "SELECT * FROM booking WHERE PickupDate >= ? AND BookingStatus = 'Confirmed'"
        today = datetime.date.today()
        booking_params = (today,)
        self.bookings = self.db.execute_query(query=booking_query, params=booking_params, fetch_all=True)
        self.db.close_connection()

        # Add an entry for each booking
        for i in range(len(self.bookings)):
            entry_layout = QHBoxLayout()
            label = QLabel(f"Booking {i}")
            entry_layout.addWidget(label)

            view_btn = QPushButton("View")
            view_btn.setFixedSize(120, 50)
            view_btn.clicked.connect(lambda _, idx=i: self.handle_view_click(idx))  # Connect button to function passing its index as a parameter
            entry_layout.addWidget(view_btn)

            scroll_layout.addLayout(entry_layout)

        # Close button to close the All Bookings window
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def handle_view_click(self, index):
        # Call view booking data with index to pull data from bookings
        self.booking_widget = BookingWidget(booking=self.bookings[index], db_path=self.db_path, is_admin=True)
        self.booking_widget.show()