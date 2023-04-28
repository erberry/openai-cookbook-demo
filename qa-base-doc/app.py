import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox
from PyQt5.QtCore import QSize
from chat_area import ChatArea
from setting import SettingArea
from building import BuildWidget
from usage import PopupUsage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set main window properties
        self.setWindowTitle('使用ChatGPT构建本地知识库')
        self.setGeometry(20, 20, 1400, 700)

        chat_area = ChatArea(self)

        right_layout = QVBoxLayout()
        settings_groupBox = SettingArea()
        self.building_groupBox = BuildWidget()
        right_layout.addWidget(settings_groupBox)
        right_layout.addWidget(self.building_groupBox)

        layout = QVBoxLayout()
        usage = QPushButton("使用说明")
        usage.clicked.connect(self.on_usage_click)

        # Add containers to main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(chat_area, 7)
        main_layout.addLayout(right_layout, 3)

        layout.addWidget(usage)
        layout.addLayout(main_layout)
        
        # Set main layout and show window
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.show()

    def on_usage_click(self):
        pop = PopupUsage()
        pop.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())