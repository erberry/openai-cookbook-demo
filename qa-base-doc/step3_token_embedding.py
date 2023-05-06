import time
import pandas as pd
import tiktoken
import openai
import sys
import os
from config import Config
from gensim.models import KeyedVectors
import jieba
import numpy as np

def token():
    ################################################################################
    ### Step 3
    ################################################################################
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv('processed/scraped.csv', index_col=0)
    df.columns = ['title', 'text']
    
    # 对文本进行分词，并将分词数保存到新列中
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    
    print(f'---------------------------分词完毕, 记录条数: {len(df)}')
    
    ################################################################################
    ### Step 4
    ################################################################################
    
    max_tokens = 500
    
    shortened = []
    
    # 遍历数据
    for row in df.iterrows():
    
        # 如果文本为空，则继续下一行
        if row[1]['text'] is None:
            continue
    
        # 如果Token数大于最大Token数，则将文本拆分为多个块
        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'], tokenizer, max_tokens)
        
        # 否则，将该文本添加到缩短文本列表中
        else:
            shortened.append( row[1]['text'] )
    
    ################################################################################
    ### Step 5
    ################################################################################
    
    df = pd.DataFrame(shortened, columns = ['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    print(f'---------------------------分词拆分完毕, 记录条数: {len(df)}')
    return df


# 将文本按照max_tokens拆分
def split_into_many(text, tokenizer, max_tokens):

    text = text.replace('。', '. ')
    # 将文本分割成句子
    sentences = text.split('. ')

    # 获取每个句子的标记数量
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    
    chunks = []
    tokens_so_far = 0
    chunk = []

    # 遍历句子和标记组成的元组
    for sentence, token in zip(sentences, n_tokens):

        # 如果到目前为止的标记数量和当前句子的标记数量之和大于最大标记数量，
        # 则将块添加到块列表中并重置块和标记数量
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # 如果当前句子的标记数大于最大标记数，则跳过该句子
        if token > max_tokens:
            continue

        # 否则，将该句子添加到块中，并将标记数加到总数
        chunk.append(sentence)
        tokens_so_far += token + 1
        
    # 将最后一个块添加到块列表中
    if chunk:
        chunks.append(". ".join(chunk) + ".")

    return chunks

################################################################################
### Step 6
################################################################################

# 注意根据您尝试嵌入的文件数量，可能会遇到速率限制问题
# 请查看速率限制指南以了解如何处理此问题: https://platform.openai.com/docs/guides/rate-limits

def progress_bar(percent, width=50):
    left = width * percent // 100
    right = width - left
    print('[' + '#' * left + ' ' * right + ']' + str(percent) + '%', end='\r')


def openai_embedding(text, fromConsole):
    embedding = openai.Embedding.create(input=text, engine='text-embedding-ada-002')['data'][0]['embedding']
    if fromConsole:
        time.sleep(1)  # 每个请求之间间隔1秒，避免超过openai接口频率上限（每分钟60次）
    return embedding

def create_embedding(row, datalen, fromConsole, model):
    index, text = row.name, row['text']
    if model == 'text-embedding-ada-002':
        ret = openai_embedding(text, fromConsole)
    else:
        ret = common_embedding(text, model)
    if fromConsole:
        progress_bar(int(index/datalen*100))
    return ret

embeddingModelLoaded = {}

def common_embedding(text, model):
    wv_model = embeddingModelLoaded.get(model)
    if wv_model is None:
        wv_model = load_embedding_model(model)
        embeddingModelLoaded[model] = wv_model

    
    vectors = get_sentence_vector(wv_model, text)
    vector_string = ", ".join(map(str, vectors.tolist()))
    return f'[{vector_string}]'

model_path = './model/'

def load_embedding_model(model):
    name_without_ext, ext = os.path.splitext(model)
    if ext == '.bin':
        binary = True
    else:
        binary = False
    print(f"begin load embedding model {model}")
    start_time = time.time()
    wv_model = KeyedVectors.load_word2vec_format(model_path+model, binary=binary)
    end_time = time.time()
    run_time = end_time - start_time
    print("end load embedding model {} {:.2f}秒".format(model, run_time))
    return wv_model

# 分词并获取文本的词向量表示
def get_sentence_vector(wv_model, sentence):
    words = jieba.lcut(sentence)
    vectors = []
    vector_size = wv_model.vector_size
    for word in words:
        if word.isspace():
            continue
        if word in wv_model:
            vectors.append(wv_model[word])
        else:
            # 如果模型中没有该词的向量表示，则用随机向量代替
            vectors.append(np.random.uniform(-0.25, 0.25, size=vector_size))
            print(f"{word} not found in embedding model")
    if len(vectors) == 0:
        return None
    else:
        return np.mean(vectors, axis=0)

def embedding(df, model):
    name_without_ext, ext = os.path.splitext(model)
    df['embeddings'] = df.apply(create_embedding, axis=1, datalen=len(df), fromConsole=True, model=model)
    fname = f'processed/embeddings-{name_without_ext}.csv'
    df.to_csv(fname)
    print(f'---------------------------Embedding完毕, 写入{fname}文件')

if __name__ == '__main__':
    Config.loadINI('./config.ini')
    model = Config.get("Embedding_Model")
    if model == 'text-embedding-ada-002':
        openai.api_key = Config.get("OPENAI_API_KEY")
    df = token()
    if input("下一步进行Embedding.是否继续？(y/n)") != 'y':
        sys.exit()
    embedding(df, model)
