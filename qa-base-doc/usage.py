from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from step4_question import answer_question
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Usage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = parent

        self.expandBtn = QPushButton("使用指南")
        self.expandBtn.setFixedSize(QSize(80,30))
        self.expandBtn.clicked.connect(self.on_expand_button_clicked)
        self.expandBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.usage_web_view = QWebEngineView(self)
        with open('usage.html', 'r') as f:
            html = f.read()
        self.usage_web_view.setHtml(html)
        self.usage_web_view.setFixedSize(1200,300)
        self.usage_web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.usage_web_view.setHidden(True)

        # button_widget = QWidget()
        # button_layout = QHBoxLayout()
        # button_layout.addWidget(self.expandBtn)
        # button_layout.addStretch(1)
        # button_widget.setLayout(button_layout)
        # button_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        # self.webview_widget = QWidget()
        # webview_layout = QHBoxLayout()
        # webview_layout.addWidget(self.usage_web_view)
        # webview_layout.addStretch(9)
        # self.webview_widget.setLayout(webview_layout)
        # self.webview_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.webview_widget.setHidden(True)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.expandBtn)
        self.main_layout.addWidget(self.usage_web_view)
        self.setLayout(self.main_layout)

    def on_expand_button_clicked(self):
        self.usage_web_view.setHidden(not self.usage_web_view.isHidden())
        if self.usage_web_view.isHidden():
            self.expandBtn.setText("使用指南")
        else:
            self.expandBtn.setText("折叠")
        self.main.update()


