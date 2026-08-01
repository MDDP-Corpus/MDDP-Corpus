# import pandas as pd
# import requests
# from tqdm import tqdm
#
# # 配置
# host = "127.0.0.1"
# port = "11434"
# url = f"http://{host}:{port}/api/chat"
# model = "llama3:8b"
# headers = {"Content-Type": "application/json"}
# input_file = r'D:\\Niutong\\数据集\\dataset.xlsx'
# output_file = r'D:\\Niutong\\数据集\\output_file.xlsx'
#
# # 读取Excel文件
# df = pd.read_excel(input_file)
# abstracts = df['abstract'].tolist()
#
# # 创建一个列表来存储模型的输出
# results = []
#
# # 使用 tqdm 显示进度条
# for abstract in tqdm(abstracts, desc="Processing abstracts", unit="abstract"):
#     data = {
#         "model": model,
#         "options": {
#             "temperature": 0.
#         },
#         "stream": False,
#         "messages": [{
#             "role": "user",
#             "content": f"The input content is the abstract content of a paper. If you think this paper is a data paper, please output 1, otherwise output 0. The abstract is as follows:{abstract}"
#         }]
#     }
#     print('指令输入成功')
#     # 发送请求
#     response = requests.post(url, json=data, headers=headers, timeout=200)
#     res = response.json()
#
#     # 提取并保存模型的输出
#     content = res['message']['content']
#     results.append(content)
#
# # 将结果写入新的Excel文件
# df['model_output'] = results
# df.to_excel(output_file, index=False)
#
# print(f"处理完成，结果已保存到 {output_file}")

#正常分类
import pandas as pd
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
host = "127.0.0.1"
port = "11434"
url = f"http://{host}:{port}/api/chat"
model = "llama3:8b"
headers = {"Content-Type": "application/json"}
input_file = r'D:\\Niutong\\数据集\\大语言模型数据\\merged_file.xlsx'
output_file = r'D:\\Niutong\\数据集\\大语言模型数据\\分类结果.xlsx'

# 读取Excel文件
df = pd.read_excel(input_file)
abstracts = df['abstract'].tolist()

# 创建一个列表来存储模型的输出
results = [None] * len(abstracts)


# 定义请求处理函数
def process_abstract(abstract, idx):
    print(f"开始处理第 {idx + 1} 个摘要...")
    data = {
        "model": model,
        "options": {
            "temperature": 0.
        },
        "stream": False,
        "messages": [{
            "role": "user",
            "content": f"The input content is the abstract content of a paper. If you think this paper is a data paper, please output 1, otherwise output 0. The abstract is as follows:{abstract}"
        }]
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=200)
        res = response.json()
        content = res['message']['content']
        print(f"第 {idx + 1} 个摘要处理完成。")
        return content
    except Exception as e:
        print(f"第 {idx + 1} 个摘要处理时出错：{e}")
        return None


# 使用 ThreadPoolExecutor 来并行处理摘要并添加进度条
with ThreadPoolExecutor(max_workers=1) as executor:
    futures = {executor.submit(process_abstract, abstract, idx): idx for idx, abstract in enumerate(abstracts)}

    for future in tqdm(as_completed(futures), total=len(abstracts), desc="Processing abstracts", unit="abstract"):
        idx = futures[future]
        results[idx] = future.result()

# 将结果写入新的Excel文件
df['model_output'] = results
df.to_excel(output_file, index=False)

print(f"处理完成，结果已保存到 {output_file}")
