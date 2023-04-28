from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from step4_question import answer_question
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from local_html import LocalHtmlViewer
import os

class PopupUsage(QDialog):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        view = LocalHtmlViewer(f'{os.getcwd()}/usage.html')
        view.show()
        layout.addWidget(view)
        self.setFixedSize(1200,600)
        self.setLayout(layout)
