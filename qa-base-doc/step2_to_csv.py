import os
import pandas as pd

################################################################################
### Step 2
################################################################################


def remove_newlines(serie):
    serie = serie.str.replace('\n', '. ')
    serie = serie.str.replace('\\n', '. ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


def toCsv():
    # 创建一个列表来存储文本文件
    texts=[]

    # 获取text目录下的所有文本文件
    for file in os.listdir("text/"):

        # 打开文件并读取文本内容
        with open("text/" + file, "r", encoding="UTF-8") as f:
            text = f.read()

            # 用空格替换-、_和#update。
            texts.append((file.replace('-',' ').replace('_', ' ').replace('#update',''), text))

    # 从文本列表创建一个DataFrame
    df = pd.DataFrame(texts, columns = ['fname', 'text'])
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv('processed/scraped.csv')

# 将文本列设置为去除换行符后的原始文本
if __name__ == '__main__':
    toCsv()
    print('---------------------------csv生成完毕，写入processed/scraped.csv文件')


