import time
import pandas as pd
import tiktoken
import openai
import sys
from config import Config

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


def create_embedding(row, param):
    index, text = row.name, row['text']
    embedding = openai.Embedding.create(input=text, engine='text-embedding-ada-002')['data'][0]['embedding']
    progress_bar(int(index/param*100))
    time.sleep(1)  # 每个请求之间间隔1秒，避免超过openai接口频率上限（每分钟60次）
    return embedding

def embedding(df):
    df['embeddings'] = df.apply(create_embedding, axis=1, param=len(df))
    df.to_csv('processed/embeddings.csv')
    print(f'---------------------------Embedding完毕, 写入processed/embeddings.csv文件')

if __name__ == '__main__':
    Config.loadINI('./config.ini')
    openai.api_key = Config.get("OPENAI_API_KEY")
    df = token()
    if input("下一步进行Embedding.是否继续？(y/n)") != 'y':
        sys.exit()
    embedding(df)
