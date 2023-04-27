from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QGroupBox
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from step4_question import loadEmbedding
from step3_token_embedding import create_embedding, token
from step2_to_csv import toCsv
from step1_to_text import parse_folder
import pandas as pd
import openai
from config import Config


class BuildWidget(QGroupBox):
    stopEmbeddingSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.df = None
        self.embedding = None
        
    def initUI(self):
        self.setTitle("构建")
        self.setFont(QFont("Arial",20))
        self.setStyleSheet("QGroupBox::title{ subcontrol-position: top center; font-size: 22pt; font-weight: bold; color: red; }")
        layout = QVBoxLayout(self)

        commentLabel = QLabel("请依序执行：提取文本->转CSV->分词->词向量")
        commentLabel.setStyleSheet("color: red;") 
        layout.addWidget(commentLabel)

        btn_layout = QHBoxLayout(self)
        
        # 创建四个按钮，并绑定槽函数
        toText = QPushButton("提取文本", self)
        toText.setObjectName("to_text")
        toText.clicked.connect(lambda: self.changeButtonText(toText))
        btn_layout.addWidget(toText)
        
        self.toCsvBtn = QPushButton("转CSV", self)
        self.toCsvBtn.setObjectName("to_csv")
        self.toCsvBtn.clicked.connect(lambda: self.changeButtonText(self.toCsvBtn))
        btn_layout.addWidget(self.toCsvBtn)

        self.toTokenBtn = QPushButton("分词", self)
        self.toTokenBtn.setObjectName("to_token")
        self.toTokenBtn.clicked.connect(lambda: self.changeButtonText(self.toTokenBtn))
        btn_layout.addWidget(self.toTokenBtn)
        
        self.toEmbeddingBtn = QPushButton("词向量", self)
        self.toEmbeddingBtn.setObjectName("to_embedding")
        self.toEmbeddingBtn.clicked.connect(lambda: self.changeButtonText(self.toEmbeddingBtn))
        btn_layout.addWidget(self.toEmbeddingBtn)

        layout.addLayout(btn_layout)
        
        # 创建进度条
        self.progressbar = QProgressBar(self)
        self.progressbar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progressbar)
        
        # 创建文本展示框
        self.textedit = QTextEdit(self)
        self.textedit.setReadOnly(True)
        self.textedit.setFont(QFont("Arial",15))
        layout.addWidget(self.textedit)
        
        self.setLayout(layout)
    
    # 改变按钮名称的槽函数
    def changeButtonText(self, button):
        if button.objectName() == "to_text":
            self.doText()
        elif button.objectName() == "to_csv":
            self.doCsv()
        elif button.objectName() == "to_token":
            self.doToken()
        elif button.objectName() == "to_embedding":
            if button.text() == "词向量":
                if self.doEmbedding():
                    button.setText("停止")
            else:
                button.setText("词向量")
                self.stopEmbeddingSignal.emit()

    def doText(self):
        self.toTokenBtn.setEnabled(False)
        self.textTask = ToTextThread()
        self.textTask.finished.connect(self.endText)
        self.textTask.start()

    def endText(self):
        self.textedit.setTextColor(QColor("green"))
        self.textedit.setText('text生成完毕，写入text文件夹')
        self.toTokenBtn.setEnabled(True)

    def doCsv(self):
        self.toCsvBtn.setEnabled(False)
        self.csvTask = ToCsvThread()
        self.csvTask.finished.connect(self.endCsv)
        self.csvTask.start()

    def endCsv(self):
        self.textedit.setTextColor(QColor("green"))
        self.textedit.setText('csv生成完毕，写入processed/scraped.csv文件')
        self.toCsvBtn.setEnabled(True)

    def doToken(self):
        self.toTokenBtn.setEnabled(False)
        self.tokenTask = ToTokenThread()
        self.tokenTask.finished.connect(self.endToken)
        self.tokenTask.start()

    def endToken(self, df):
        self.textedit.setTextColor(QColor("green"))
        self.textedit.setText(f"分词拆分完毕, 记录条数: {len(df)}")
        self.df = df
        self.toTokenBtn.setEnabled(True)

    def doEmbedding(self):
        if self.df is None:
            self.textedit.setTextColor(QColor("red"))
            self.textedit.setText("没有分词数据，请先进行分词")
            return False
        self.embedding = None
        self.embeddingTask = ToEmbeddingThread(self.df)
        self.stopEmbeddingSignal.connect(self.embeddingTask.onStop)
        self.embeddingTask.progressUpdated.connect(self.progressbarUpdate)
        self.embeddingTask.finished.connect(self.endEmbedding)
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(len(self.df))
        self.progressbar.setValue(0)
        self.embeddingTask.start()
        return True

    def endEmbedding(self):
        self.df = None
        self.textedit.setTextColor(QColor("green"))
        self.textedit.setText("Embedding完毕, 写入processed/embeddings.csv文件")
        self.embedding = loadEmbedding()

    def progressbarUpdate(self, index):
        self.progressbar.setValue(index)

class ToTextThread(QThread):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        parse_folder('doc', 'text')
        self.finished.emit()

class ToCsvThread(QThread):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        toCsv()
        self.finished.emit()

class ToTokenThread(QThread):
    finished = pyqtSignal(pd.DataFrame)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        df = token()
        self.finished.emit(df)

class ToEmbeddingThread(QThread):
    progressUpdated = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.df = df
        self.stop = False

    @pyqtSlot()
    def onStop(self):
        self.stop = True
        pass

    def run(self):
        openai.api_key = Config.get("OPENAI_API_KEY")
        embs = []
        for index, row in self.df.iterrows():
            if self.stop:
                break
            emb = create_embedding(row, param=len(self.df))
            embs.append(emb)
            # 更新进度条
            self.progressUpdated.emit(index)

        valid = self.df.head(len(embs))
        valid['embeddings'] = embs
        valid.to_csv('processed/embeddings.csv')
        self.finished.emit()
        print(f'---------------------------Embedding完毕{len(embs)}条, 写入processed/embeddings.csv文件')