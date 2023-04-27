from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ChatList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setWordWrap(True)

    def add_message(self, sender, content, sent_time):
        item1 = QListWidgetItem(f"{sender} {sent_time}")
        item2 = QListWidgetItem(content)
        
        self.addItem(item1)
        self.addItem(item2)

        # 让窗口自动滚动到最新的消息处
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class ChatArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = parent
        chat_container_layout = QVBoxLayout()

        self.chat_list = ChatList()
        self.question_input = QLineEdit("这里输入问题...")
        self.send_button = QPushButton("发送")
        self.clear_button = QPushButton("清空")
        self.clear_button.clicked.connect(self.on_clear_button_clicked)
        self.send_button.clicked.connect(self.on_send_button_clicked)
        chat_container_layout.addWidget(self.chat_list)
        send_layout = QHBoxLayout()
        send_layout.addWidget(self.question_input)
        send_layout.addWidget(self.send_button)
        send_layout.addWidget(self.clear_button)
        chat_container_layout.addLayout(send_layout)
        self.setLayout(chat_container_layout)

    def on_send_button_clicked(self):
        if self.main.building_groupBox.embedding is None:
            msg_box = QMessageBox()
            msg_box.setText("没有生成词向量，请按照右侧构建步骤进行")
            msg_box.setWindowTitle("提示信息")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.exec_()
            return
    
        self.send_button.setEnabled(False)
        text = self.question_input.text()
        self.question_input.clear()
        self.chat_list.add_message("我", text, "111")
        self.answer(text)


    def on_clear_button_clicked(self):
        self.chat_list.clear()

    def answer(self, question):
        task = AnswerThread()

        

class AnswerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.finished.emit()