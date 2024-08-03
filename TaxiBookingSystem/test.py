import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt


#Function to display a message box with "Hello World!" content
def display_msg():
    QMessageBox.information(None, "Message", "Hello World!")

#Create QApplication
app = QApplication(sys.argv)

#Create Main Window
window = QWidget()
window.setWindowTitle("Taxi Booking System")
window.setFixedSize(800, 600)

#Create Vertical Layout
v_layout = QVBoxLayout()

#Create Label Widget
label = QLabel("Welcome to the Taxi Booking System!")
label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

#Add Label to Vertical Layout
v_layout.addWidget(label)

#Create Horizontal Layout for Buttons
h_layout = QHBoxLayout()

#Add Horizontal Layout to Vertical Layout
v_layout.addLayout(h_layout)

#Create Login Button
login_btn = QPushButton("Login")
login_btn.clicked.connect(display_msg)

#Add Login Button to Horizontal Layout
h_layout.addWidget(login_btn)

#Create Register Button
register_btn = QPushButton("Register")
register_btn.clicked.connect(display_msg)

#Add Register Button to Horizontal Layout
h_layout.addWidget(register_btn)

#Create Exit Button
exit_btn = QPushButton("Exit")
exit_btn.clicked.connect(app.quit)

#Add Exit Button to Horizontal Layout
h_layout.addWidget(exit_btn)

#Add Vertical Layout to Main Window
window.setLayout(v_layout)

#Display Main Window
window.show()

#Start the event loop and wait for user interaction
sys.exit(app.exec())