import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox
from chat_area import ChatArea
from setting import SettingArea
from building import BuildWidget
from config import Config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set main window properties
        self.setWindowTitle('My Chatbot')
        self.setGeometry(50, 50, 1400, 800)

        chat_area = ChatArea(self)

        right_layout = QVBoxLayout()
        settings_groupBox = SettingArea()
        self.building_groupBox = BuildWidget()
        right_layout.addWidget(settings_groupBox)
        right_layout.addWidget(self.building_groupBox)


        # Add containers to main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(chat_area, 7)
        main_layout.addLayout(right_layout, 3)
        
        # Set main layout and show window
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())