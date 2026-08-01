# _*_ coding : utf-8 _*_

import os
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        article_element = []
        # 文章题目
        meta_tag1 = soup.find('meta', {'name': 'dc.title'})
        title = meta_tag1['content']
        article_element.append(title)

        # 文章DOI
        meta_tag2 = soup.find('meta', {'name': 'prism.doi'})
        doi = None  # Default value if 'meta_tag2' is None
        if meta_tag2 is not None:
            doi = meta_tag2.get('content', None)
        article_element.append(doi)
        # 出版商
        meta_tag3 = soup.find('meta', {'name': 'dc.publisher'})
        publisher = meta_tag3['content']
        if publisher:
            article_element.append(publisher)
        else:
            article_element.append('0')
        # 期刊名
        meta_tag4 = soup.find('meta', {'name': 'prism.publicationName'})
        journal = meta_tag4['content']
        if journal:
            article_element.append(journal)
        else:
            article_element.append('0')
        # 出版日期
        meta_tag5 = soup.find('meta', {'name': 'prism.publicationDate'})
        date = meta_tag5['content']
        if date:
            article_element.append(date)
        else:
            article_element.append('0')
        # 文章类型
        meta_tag6 = soup.find('meta', {'name': 'citation_article_type'})
        article_type = meta_tag6['content']
        if article_type:
            article_element.append(article_type)
        else:
            article_element.append('0')
        # 作者
        meta_tag7 = soup.find_all('meta', {'name': 'dc.creator'})
        article_creator = [tag['content'] for tag in meta_tag7]
        if article_creator:
            article_element.append(article_creator)
        else:
            article_creator.append('0')
        # 文章主题
        meta_tag8 = soup.find_all('meta', {'name': 'dc.subject'})
        article_type = [tag['content'] for tag in meta_tag8]
        if article_type:
            article_element.append(article_type)
        else:
            article_element.append('0')
        # 摘要内容
        abstract_div = soup.find('div', {'class': 'c-article-section__content', 'id': 'Abs1-content'})
        if abstract_div:
            abstract_content = abstract_div.get_text(strip=True)
            article_element.append(abstract_content)
        else:
            article_element.append('空')

        # 一级标题
        main_content_div = soup.find('div', {'class': 'main-content'})
        sections = soup.find_all('section', {'data-title': True})
        h2_tags = soup.find_all(
            'h2', {'class': 'c-article-section__title js-section-title js-c-reading-companion-sections-item',
                   'id': 'further-reading'})
        # 提取 data-title 的值并存储到列表中
        data_titles = [section['data-title'] for section in sections] + [h2.text.strip() if h2.text.strip() else None for h2 in h2_tags]
        article_element.append(data_titles)


        # 二级标题
        h3_tags = soup.find_all('h3', class_='c-article__sub-heading')
        # 提取<h3>标签的文本内容并保存到列表中
        sub_headings = [tag.get_text(strip=True) for tag in h3_tags]
        article_element.append(sub_headings)

        # 三级标题
        h4_tags = soup.find_all('h4', class_='c-article__sub-heading c-article__sub-heading--small')
        # 提取<h3>标签的文本内容并保存到列表中
        sub_headings_small = [tag.get_text(strip=True) for tag in h4_tags]
        article_element.append(sub_headings_small)
        return article_element

def process_folder(input_folder, output_folder):
    data = []

    # 获取文件数量以用于进度条
    file_count = len([file_name for file_name in os.listdir(input_folder) if file_name.endswith(".html")])

    for file_name in tqdm(os.listdir(input_folder), total=file_count, desc="Processing HTML files"):
        if file_name.endswith(".html"):
            file_path = os.path.join(input_folder, file_name)
            parsed_data = parse_html(file_path)

            if parsed_data:
                data.append({'文件名': file_name, '标题': parsed_data[0], 'DOI': parsed_data[1],
                             '出版商': parsed_data[2], '期刊名': parsed_data[3],
                             '出版日期': parsed_data[4], '文章类型': parsed_data[5],
                             '作者': parsed_data[6], '文章主题': parsed_data[7],
                             '摘要': parsed_data[8], '一级标题': parsed_data[9],
                             '二级标题': parsed_data[10], '三级标题': parsed_data[11]})

    if data:
        df = pd.DataFrame(data)
        output_file = os.path.join(output_folder, 'output.xlsx')
        df.to_excel(output_file, index=False)
        print(f"Excel file saved at: {output_file}")
    else:
        print("No valid data found in HTML files.")


# 指定输入和输出文件夹
input_folder = 'F:\\Datapaper\\试验数据\\html'
output_folder = 'F:\\Datapaper\\试验数据\\篇章结构抽取试验结果'

# 处理文件夹中的HTML文件并生成Excel文件
process_folder(input_folder, output_folder)
