# _*_ coding : utf-8 _*_
import os
import PyPDF2
from tqdm import tqdm


def convert_pdf_to_xml(pdf_path, output_folder):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        xml_content = f"<?xml version='1.0' encoding='UTF-8'?><pdf>{os.path.basename(pdf_path)}</pdf>"
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            xml_content += f"<page>{text}</page>"

    output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(pdf_path))[0] + ".xml")
    with open(output_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(xml_content)


def batch_convert_pdfs_to_xml(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [file for file in os.listdir(input_folder) if file.endswith(".pdf")]
    for file in tqdm(pdf_files, desc="Converting PDFs", unit="file"):
        pdf_path = os.path.join(input_folder, file)
        convert_pdf_to_xml(pdf_path, output_folder)


# 指定输入文件夹和输出文件夹
input_folder = "F:\\Datapaper\\Data in Brief（pdf）\\ScienceDirect_articles_15Nov2023_01-28-44.115"
output_folder = "F:\\Datapaper\\试验数据\\xml"

batch_convert_pdfs_to_xml(input_folder, output_folder)

