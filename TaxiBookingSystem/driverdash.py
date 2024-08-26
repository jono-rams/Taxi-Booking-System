from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from connection import Database
from driverviewbookings import ViewBookings


class DriverDashboard(QWidget):

    def handle_view(self):
        self.vb = ViewBookings(driver_id=self.id, dash_reference=self)
        self.vb.show()
        self.hide()

    def __init__(self, driver_id):
        super().__init__()

        self.vb = None

        self.id = driver_id
        self.name = None
        self.plate_no = None
        self.email = None
        self.password = None
        self.status = None
        self.license_no = None
        self.license_exp = None

        self.db = Database()
        self.db.connect("db/test.db")
        driver_query = "SELECT * FROM driver WHERE driverID =?"
        driver = self.db.execute_query(query=driver_query, params=driver_id)
        if driver:
            self.id, self.name, self.email, self.plate_no, self.password, self.status, self.license_no, self.license_exp = driver
        else:
            raise Exception("Could not find driver")
        self.db.close_connection()

        self.setWindowTitle("Driver Dashboard")

        v_layout = QVBoxLayout()

        # Create Label Widget
        label = QLabel(f"Welcome {self.name}!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        font = QFont()
        font.setPointSize(20)
        font.setFamily("TimesNewRoman")
        label.setFont(font)
        label.setFixedHeight(35)

        # Add Label to Vertical Layout
        v_layout.addWidget(label)

        # Create Horizontal Layout for Buttons
        buttons_layout = QHBoxLayout()

        # Create Login Button
        self.view_book_btn = QPushButton("View Bookings")
        self.view_book_btn.clicked.connect(self.handle_view)

        # Add Login Button to Button Layout
        buttons_layout.addWidget(self.view_book_btn)

        # Create Close Button
        self.close_btn = QPushButton("Logout")
        self.close_btn.clicked.connect(self.close)

        # Add Close Button to Button Layout
        buttons_layout.addWidget(self.close_btn)

        # Add Buttons to Vertical Layout
        v_layout.addLayout(buttons_layout)

        # Set Vertical Layout to Main Window
        self.setLayout(v_layout)
