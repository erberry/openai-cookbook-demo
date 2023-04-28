from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from step4_question import answer_question
import datetime
from config import Config
import openai

class ChatList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setWordWrap(True)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def add_message(self, sender, content, sent_time):
        item1 = QListWidgetItem(f"{sender} {sent_time}")
        item1.setFont(QFont("Arial",10))
        item1.setForeground(QColor(0x666666))
        item2 = QListWidgetItem(content)
        item2.setBackground(QBrush(QColor(0xf2f2f2)))
        
        self.addItem(item1)
        self.allowCopy(item1)
        self.addItem(item2)
        self.allowCopy(item2)

        # 让窗口自动滚动到最新的消息处
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def allowCopy(self, item):
        # 允许复制
        item.setFlags(item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled )

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # 自己定义右键弹出菜单的内容和行为
            menu = QMenu(self)
            copy_action = menu.addAction("复制")
            copy_all_action = menu.addAction("复制全部")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action == copy_action:
                clipboard = QApplication.clipboard()
                all_text = [item.text() for item in (self.selectedItems())]
                clipboard.setText('\n'.join(all_text))
            elif action == copy_all_action:
                clipboard = QApplication.clipboard()
                all_text = [self.item(i).text() for i in range(self.count())]
                clipboard.setText('\n'.join(all_text))
        else:
            super(ChatList, self).mousePressEvent(event)

class ChatArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = parent
        chat_container_layout = QVBoxLayout()

        self.chat_list = ChatList()
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("这里输入问题...")
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
        if Config.getEmbedding() is None:
            msg_box = QMessageBox()
            msg_box.setText("没有生成词向量，请按照右侧构建步骤进行")
            msg_box.setWindowTitle("提示信息")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.exec_()
            return
    
        self.send_button.setEnabled(False)
        text = self.question_input.text()
        self.question_input.clear()
        self.addMessage(text, "我：")
        self.question(text, Config.getEmbedding())


    def on_clear_button_clicked(self):
        self.chat_list.clear()

    def question(self, question, embedding):
        self.task = AnswerThread(question, embedding)
        self.task.finished.connect(self.answer)
        self.task.start()

    def answer(self, answer):
        self.addMessage(answer, "AI：")
        self.send_button.setEnabled(True)

    def addMessage(self, text, role):
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.chat_list.add_message(role, text, current_time)


class AnswerThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, question, embedding, parent=None):
        super().__init__(parent)
        self.question = question
        self.embedding = embedding

    def run(self):
        try:
            openai.api_key = Config.get('openai_api_key')
            a = answer_question(
                self.embedding, 
                model = Config.get("MODEL"),
                max_len = int(Config.get("CONTEXT_MAX_TOKEN")),
                max_tokens = int(Config.get("MAX_TOKEN")),
                question=self.question, 
                debug=False
            )
        except Exception as e:
            print("发生了未知异常，错误信息为:", e)
            self.finished.emit(f"发生了未知异常，错误信息为: {e}")
            return
        self.finished.emit(a)
        