from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from config import Config

class SettingArea(QGroupBox):
    def __init__(self):
        super().__init__()
        Config.loadINI("./config.ini")
        self.setDefaultConfig()

        self.setTitle("设置")
        self.setFont(QFont("Arial",20))
        self.setStyleSheet("QGroupBox::title{ subcontrol-position: top center; font-size: 22pt; font-weight: bold; color: green; }")

        apik_main_layout = QHBoxLayout()
        api_key_label = QLabel("API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.resize(50, 10)
        apik_main_layout.addWidget(api_key_label, 2)
        apik_main_layout.addWidget(self.api_key_input, 8)
        self.api_key_input.setText(Config.get("OPENAI_API_KEY"))

        max_token_main_layout = QHBoxLayout()
        max_token_label = QLabel("Max Token:")
        self.max_token_input = QLineEdit()
        self.max_token_input.resize(50, 10)
        max_token_main_layout.addWidget(max_token_label, 2)
        max_token_main_layout.addWidget(self.max_token_input, 8)
        self.max_token_input.setText(Config.get("MAX_TOKEN"))

        save_button = QPushButton("保存设置")
        save_button.clicked.connect(self.save)

        settings_container_layout = QVBoxLayout()
        settings_container_layout.addLayout(apik_main_layout, 1)
        settings_container_layout.addLayout(max_token_main_layout, 1)
        settings_container_layout.addWidget(save_button, 1)
        settings_container_layout.addStretch()
        
        self.setLayout(settings_container_layout)

    def setDefaultConfig(self):
        if Config.get("MAX_TOKEN") == '':
            Config.set("MAX_TOKEN", 2048)

    def save(self):
        Config.set("OPENAI_API_KEY", self.api_key_input.text())
        Config.set("MAX_TOKEN", self.max_token_input.text())
        Config.save()
        pass