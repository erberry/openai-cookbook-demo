import configparser
import pandas as pd
import numpy as np
import os

class Config:
    config = configparser.ConfigParser()
    path = ''
    embedding = None

    @classmethod
    def loadINI(cls, path):
        cls.path = path
        cls.config.read(path)

    @classmethod
    def get(cls, key, section='default'):
        return cls.config.get(section, key)
    
    @classmethod
    def set(cls, key, val, section='default'):
        cls.config.set(section, key, val)

    @classmethod
    def save(cls):
        with open(cls.path, 'w') as configfile:
            cls.config.write(configfile)

    @classmethod
    def getEmbedding(cls):
        if cls.embedding is None:
            try:
                cls.loadEmbedding()
            except Exception as e:
                print("发生了未知异常，错误信息为:", e)
                return None
        return cls.embedding
    
    @classmethod
    def loadEmbedding(cls):
        model = cls.get("Embedding_Model")
        name_without_ext, ext = os.path.splitext(model)
        df=pd.read_csv(f'processed/embeddings-{name_without_ext}.csv', index_col=0)
        df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
        cls.embedding = df
    
    @classmethod
    def clearEmbedding(cls):
        cls.embedding = None

