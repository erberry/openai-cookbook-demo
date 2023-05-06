from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QComboBox
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
        api_key_label = QLabel("ⓘAPI Key:")
        api_key_label.setToolTip('OpenAI API KEY')
        self.api_key_input = QLineEdit()
        self.api_key_input.resize(50, 10)
        apik_main_layout.addWidget(api_key_label, 2)
        apik_main_layout.addWidget(self.api_key_input, 8)
        self.api_key_input.setText(Config.get("OPENAI_API_KEY"))

        max_token_main_layout = QHBoxLayout()
        max_token_label = QLabel("ⓘ最大Token数量:")
        max_token_label.setToolTip('OpenAI 接口的max_tokens参数，影响生成内容的长度。\n 可以理解为这个值减去上下文长度就是能够生成的内容的最大长度')
        self.max_token_input = QLineEdit()
        self.max_token_input.resize(50, 10)    
        max_token_main_layout.addWidget(max_token_label, 2)
        max_token_main_layout.addWidget(self.max_token_input, 8)
        self.max_token_input.setText(Config.get("MAX_TOKEN"))

        context_max_token_main_layout = QHBoxLayout()
        context_max_token_label = QLabel("ⓘ上下文最大Token数量:")
        context_max_token_label.setToolTip('从本地知识库中选取的文本的最大长度')
        self.context_max_token_input = QLineEdit()
        self.context_max_token_input.resize(50, 10)
        context_max_token_main_layout.addWidget(context_max_token_label, 2)
        context_max_token_main_layout.addWidget(self.context_max_token_input, 8)
        self.context_max_token_input.setText(Config.get("CONTEXT_MAX_TOKEN"))

        model_main_layout = QHBoxLayout()
        model_label = QLabel("ⓘ选择GPT模型:")
        model_label.setToolTip('建议选择gpt-3.5-turbo，更高效，更省token')
        self.combo_box = QComboBox()
        self.combo_box.addItem('gpt-3.5-turbo')
        self.combo_box.addItem('text-davinci-003')
        model_main_layout.addWidget(model_label, 2)
        model_main_layout.addWidget(self.combo_box, 8)
        self.combo_box.setCurrentText(Config.get("MODEL"))

        embedding_model_layout = QHBoxLayout()
        embedding_model_label = QLabel("ⓘ选择词向量计算的模型:")
        embedding_model_label.setToolTip('默认使用openai的text-embedding-ada-002 会消耗token \n 可以自行下载模型保存到model文件夹下 \n 并在此输入整个模型的文件名（包括扩展名 支持.txt或者.bin）\n 支持任何word2vec支持的模型 \n 注意：模型文件一般比较大，加载模型的时间也会长，如果是文本模型文件，可以使用tobin.py转换为二进制文件来加快加载速度')
        self.embedding_model_input = QLineEdit()
        self.embedding_model_input.resize(50, 10)
        embedding_model_layout.addWidget(embedding_model_label, 2)
        embedding_model_layout.addWidget(self.embedding_model_input, 8)
        self.embedding_model_input.setText(Config.get("Embedding_Model"))

        sleep_main_layout = QHBoxLayout()
        sleep_label = QLabel("ⓘ计算词向量间隔:")
        sleep_label.setToolTip('由于OpenAI的Embedding接口有调用速率限制，这里需要设置接口调用的间隔，默认1秒没有问题。\n 请查看速率限制指南以了解如何处理此问题: https://platform.openai.com/docs/guides/rate-limits')
        self.sleep_input = QLineEdit("1")
        self.sleep_input.resize(50, 10)
        sleep_main_layout.addWidget(sleep_label, 2)
        sleep_main_layout.addWidget(self.sleep_input, 8)
        self.sleep_input.setText(Config.get("Embedding_SLEEP_SECOND"))

        save_button = QPushButton("应用设置")
        save_button.clicked.connect(self.save)

        settings_container_layout = QVBoxLayout()
        settings_container_layout.addLayout(apik_main_layout, 1)
        settings_container_layout.addLayout(max_token_main_layout, 1)
        settings_container_layout.addLayout(context_max_token_main_layout, 1)
        settings_container_layout.addLayout(model_main_layout, 1)
        settings_container_layout.addLayout(embedding_model_layout, 1)
        settings_container_layout.addLayout(sleep_main_layout, 1)
        settings_container_layout.addWidget(save_button, 1)
        settings_container_layout.addStretch()
        
        self.setLayout(settings_container_layout)

    def setDefaultConfig(self):
        if Config.get("MAX_TOKEN") == '':
            Config.set("MAX_TOKEN", 2048)
        if Config.get("CONTEXT_MAX_TOKEN") == '':
            Config.set("CONTEXT_MAX_TOKEN", 1000)
        if Config.get("MODEL") == '':
            Config.set("MODEL", 'gpt-3.5-turbo')
        if Config.get("Embedding_SLEEP_SECOND") == '':
            Config.set("Embedding_SLEEP_SECOND", 1)
        if Config.get("Embedding_Model") == '':
            Config.set("Embedding_Model", 'text-embedding-ada-002')

    def save(self):
        Config.set("OPENAI_API_KEY", self.api_key_input.text())
        Config.set("MAX_TOKEN", self.max_token_input.text())
        Config.set("CONTEXT_MAX_TOKEN", self.context_max_token_input.text())
        Config.set("MODEL", self.combo_box.currentText())
        Config.set("Embedding_SLEEP_SECOND", self.sleep_input.text())
        Config.set("Embedding_Model", self.embedding_model_input.text())
        Config.save()
        pass