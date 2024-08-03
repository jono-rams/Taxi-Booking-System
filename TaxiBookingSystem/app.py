import sys
from PyQt6.QtWidgets import QApplication
from login import LoginWidget
class App():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = LoginWidget(app = self.app)


    def run_app(self):
        self.login_window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = App()
    app.run_app()
