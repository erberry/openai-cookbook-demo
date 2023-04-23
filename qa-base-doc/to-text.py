import os
import re
from bs4 import BeautifulSoup

################################################################################
### Step 1
################################################################################

def remove_center_tag(soup):
    # 移除center标签及其内容
    for center_tag in soup.find_all('center'):
        center_tag.extract()

def parse_html_file(html_file_path, save_text_folder):
    # 读取html文件内容
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    # 使用BeautifulSoup解析html文件
    soup = BeautifulSoup(html_content, 'html.parser')
    # 去除center标签（印象笔记导出后在center标签中包含了一大串不可读的字符）
    remove_center_tag(soup)
    # 获取html文件名称
    html_file_name = os.path.basename(html_file_path)
    # 去除html后缀
    html_file_name = re.sub(r'\.html$', '', html_file_name)
    # 拼接text文件路径
    text_file_path = os.path.join(save_text_folder, f'{html_file_name}.txt')
    # 打开text文件并写入解析后的文本内容
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(soup.get_text())

def parse_html_folder(html_folder_path, save_text_folder):
    # 遍历html文件夹下的所有.html文件
    for root, _, files in os.walk(html_folder_path):
        for file in files:
            if file.endswith('.html'):
                # 获取html文件路径
                html_file_path = os.path.join(root, file)
                print(f'提取{html_file_path}到文本...')
                # 解析html文件并写入文本文件
                parse_html_file(html_file_path, save_text_folder)
                
# 读取doc目录下的.html文件，提取其中的文本，写入text文件夹下
parse_html_folder('doc', 'text')
print('---------------------------text生成完毕，写入text文件夹')
