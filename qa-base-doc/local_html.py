from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QDesktopServices
import sys

class LocalHtmlViewer(QWidget):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle('Local HTML Viewer')
        self.setWindowIcon(QIcon('icon.png'))
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.browser = QWebEngineView()
        self.page = MyWebEnginePage(self.browser) 
        self.browser.setPage(self.page)
        self.browser.setUrl(QUrl.fromLocalFile(url))
        layout.addWidget(self.browser)

# 继承自QWebEnginePage，重写createWindow函数
class MyWebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        new_page = MyWebEnginePage(self)
        new_page.setUrl(self.lastHoveredLink())
        new_view = QWebEngineView()
        new_view.setPage(new_page)
        new_view.show()
        return new_page

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked and isMainFrame:
            QDesktopServices.openUrl(url) # 使用默认浏览器打开链接
            return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)
