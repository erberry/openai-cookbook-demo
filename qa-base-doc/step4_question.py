import os
import pandas as pd
import openai
import numpy as np
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
from config import Config

################################################################################
### Step 7
################################################################################

def loadEmbedding():
    df=pd.read_csv('processed/embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
    return df


################################################################################
### Step 8
################################################################################

def create_context(
    question, df, max_len=1800, size="ada"
):
    """
    从数据中找到最相似的上下文，为一个问题创建一个背景
    """

    # 获取该问题的 embeddings 
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # 从这些embeddings中获取距离 
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')


    returns = []
    cur_len = 0

    # 按照距离排序，并将文本添加到背景中，直到context太长为止
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        # 将文本的长度添加到当前长度中
        cur_len += row['n_tokens'] + 4
        
        # 如果上下文太长，就中断
        if cur_len > max_len:
            break
        
        # 否则将该文本添加到正在返回的文本中
        returns.append(row["text"])

    # 返回上下文
    return "\n\n###\n\n".join(returns)

def answer_question(
    df,
    model="gpt-3.5-turbo",#"text-davinci-003",
    question="",
    max_len=500,
    size="ada",
    debug=False,
    max_tokens=2500,
    stop_sequence=None
):
    """
    基于数据文本中最相似的上下文回答问题
    """

    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    # 如果是调试模式，打印原始的模型响应
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # 使用问题和上下文创建一个完成请求
        if model == 'gpt-3.5-turbo':
            completion = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "user", "content": f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nPlease speak the language in the Context\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:"}
                ],
                temperature=0,
                top_p=0.1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=stop_sequence,
            )
            return completion.choices[0].message.content

        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nPlease speak the language in the Context\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""

################################################################################
### Step 9
################################################################################

if __name__ == '__main__':
    Config.loadINI('./config.ini')
    openai.api_key = Config.get("OPENAI_API_KEY")
    df = loadEmbedding()
    while True:
        q = input("请输入你的问题（直接回车退出）：")
        if q == '':
            break  # 如果输入为空，则退出循环
        print(f'Question: {q}')
        a = answer_question(df, question=q, debug=False)
        print(f'Answer: {a}')