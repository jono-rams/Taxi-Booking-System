from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QScrollArea, \
    QFormLayout, QLineEdit, QMessageBox, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt, QSize
from adminviewupcoming import UpcomingBookings
from adminviewpending import PendingBookings
from viewdrivers import AllDriversWindow


# Main admin window class
class AdminWindow(QWidget):
    def __init__(self, admin_id, db_path):
        super().__init__()
        self.admin_id = admin_id
        self.db_path = db_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Administrator Dashboard")
        self.setGeometry(100, 100, 700, 400)

        grid = QGridLayout()

        # Update the title label with a contrasting color
        title = QLabel("Administrator Dashboard")
        title.setFont(QFont('Helvetica', 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #ffffff; background-color: rgba(0, 0, 0, 0.5); padding: 10px;")
        grid.addWidget(title, 0, 0, 1, 2)

        # Update buttons with rounded corners
        btn_style = "background-color: #000000; padding: 10px; color: yellow; border-radius: 10px;"

        btn_view_all_bookings = QPushButton('View All Bookings')
        btn_view_all_bookings.setFont(QFont('Helvetica', 12))
        btn_view_all_bookings.setStyleSheet(btn_style)
        btn_view_all_bookings.clicked.connect(self.showBookingOptions)
        grid.addWidget(btn_view_all_bookings, 1, 0)

        btn_view_drivers = QPushButton('View Drivers')
        btn_view_drivers.setFont(QFont('Helvetica', 12))
        btn_view_drivers.setStyleSheet(btn_style)
        btn_view_drivers.clicked.connect(self.viewDrivers)
        grid.addWidget(btn_view_drivers, 1, 1)

        btn_log_out = QPushButton('Log Out')
        btn_log_out.setFont(QFont('Helvetica', 12))
        btn_log_out.setStyleSheet("background-color: #000000; padding: 10px; color: red; border-radius: 10px;")
        btn_log_out.clicked.connect(self.logOut)
        grid.addWidget(btn_log_out, 2, 0, 1, 2)

        self.setLayout(grid)

    def showBookingOptions(self):
        options_dialog = QMessageBox()
        options_dialog.setWindowTitle("View Bookings Options")
        options_dialog.setText("Choose an option:")
        options_dialog.setIcon(QMessageBox.Icon.Information)

        btn_upcoming = QPushButton("View Upcoming Bookings")
        btn_upcoming.clicked.connect(self.viewUpcomingBookings)
        options_dialog.addButton(btn_upcoming, QMessageBox.ButtonRole.ActionRole)

        btn_pending = QPushButton("View Pending Bookings")
        btn_pending.clicked.connect(self.viewPendingBookings)
        options_dialog.addButton(btn_pending, QMessageBox.ButtonRole.ActionRole)

        options_dialog.exec()

    def viewUpcomingBookings(self):
        self.filtered_window = UpcomingBookings(self.db_path)
        self.filtered_window.show()

    def viewPendingBookings(self):
        self.filtered_window = PendingBookings(self.db_path)
        self.filtered_window.show()

    def viewDrivers(self):
        self.drivers_window = AllDriversWindow(self.db_path)
        self.drivers_window.show()

    def logOut(self):
        self.close()

    def closeEvent(self, event):
        event.accept()
