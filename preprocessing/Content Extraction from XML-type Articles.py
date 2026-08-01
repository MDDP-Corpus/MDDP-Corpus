# _*_ coding : utf-8 _*_

import os
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm

def extract_xml_content(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'xml')

    journal_title = soup.find('journal-title').text.strip() if soup.find('journal-title') else None
    publisher_name = soup.find('publisher-name').text.strip() if soup.find('publisher-name') else None
    article_title_elem = soup.find('article-title')
    article_title = article_title_elem.text.strip().replace('\n', '') if article_title_elem else None

    abstract_elem = soup.find('abstract')
    abstract_text = abstract_elem.get_text(separator=' ').strip().replace('\n', ' ') if abstract_elem else None
    abstract_text = abstract_text.replace('<br>', '').replace('<br/>', '') if abstract_text else None

    doi_elem = soup.find('article-id', attrs={'pub-id-type': 'doi'})
    doi = doi_elem.text.strip() if doi_elem else None

    # 提取 Publication Date
    pub_date_elem = soup.find('pub-date', attrs={'pub-type': 'epub'})
    if pub_date_elem:
        day = pub_date_elem.find('day').text.strip() if pub_date_elem.find('day') else None
        month = pub_date_elem.find('month').text.strip() if pub_date_elem.find('month') else None
        year = pub_date_elem.find('year').text.strip() if pub_date_elem.find('year') else None
        pub_date = f'{year}-{month}-{day}' if all([day, month, year]) else None
    else:
        # 从 <pub-date> 中提取 Publication Date
        pub_date_elem = soup.find('pub-date')
        if pub_date_elem:
            day = pub_date_elem.find('day').text.strip() if pub_date_elem.find('day') else None
            month = pub_date_elem.find('month').text.strip() if pub_date_elem.find('month') else None
            year = pub_date_elem.find('year').text.strip() if pub_date_elem.find('year') else None
            pub_date = f'{year}-{month}-{day}' if all([day, month, year]) else None
        else:
            pub_date = None

    # 提取所有<title>标签中的内容
    titles = [title.text.strip().replace('\n', '') for title in soup.find_all('title')]

    return journal_title, publisher_name, article_title, abstract_text, doi, pub_date, titles


def process_xml_files(input_folder, output_file):
    xml_files = [filename for filename in os.listdir(input_folder) if filename.endswith('.xml')]

    with open(output_file + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['XML File', 'Journal Title', 'Publisher Name', 'Article Title', 'Abstract', 'DOI', 'Publication Date', 'Titles']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename in tqdm(xml_files, desc='Processing XML files'):
            xml_file = os.path.join(input_folder, filename)
            journal_title, publisher_name, article_title, abstract, doi, pub_date, titles = extract_xml_content(xml_file)

            # 写入CSV文件
            writer.writerow({'XML File': filename,
                             'Journal Title': journal_title,
                             'Publisher Name': publisher_name,
                             'Article Title': article_title,
                             'Abstract': abstract,
                             'DOI': doi,
                             'Publication Date': pub_date,
                             'Titles': titles})


# 指定输入文件夹路径和输出CSV文件路径
input_folder = 'F:\\Datapaper\\ESSD'
output_file = 'F:\\Datapaper\\试验数据\\篇章结构抽取试验结果\\output'

# 处理xml文件并输出为CSV文件，并显示提取进度
process_xml_files(input_folder, output_file)
