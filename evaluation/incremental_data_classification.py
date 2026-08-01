import numpy as np
import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
import torch.nn as nn
import os


# 定义BERT分类器
class BERTClassifier(nn.Module):
    def __init__(self):
        super(BERTClassifier, self).__init__()
        self.fc = nn.Linear(768, 2)  # BERT输出的特征向量长度为768，输出维度为2

    def forward(self, x):
        x = self.fc(x)
        return x


# 配置路径
incremental_data_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\分类数据\\增量数据\\Biodiversity data journal-before.xlsx'  # 增量数据路径
model_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\训练好的模型\\scibert\\BERT_model_fold_5.pth'  # 保存的模型路径
tokenizer_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\SciBert'  # 分词器路径

# 加载增量数据
incremental_df = pd.read_excel(incremental_data_path, engine='openpyxl')

# 确保摘要列没有空值，并且是字符串类型
incremental_df = incremental_df.dropna(subset=['abstract'])  # 删除空值
incremental_df['abstract'] = incremental_df['abstract'].astype(str)  # 确保是字符串类型

incremental_abstracts = incremental_df['abstract'].tolist()

# 加载分词器和模型
tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
model = BERTClassifier()

# 初始化设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)  # 将模型移动到指定设备

# 加载已保存的模型
model.load_state_dict(torch.load(model_path, map_location=device))  # 将模型加载到正确的设备
model.eval()  # 设置模型为评估模式


# 将摘要转换为BERT特征向量
def get_bert_embeddings(abstracts):
    features = []
    for abstract in abstracts:
        if not isinstance(abstract, str):  # 确保摘要是字符串
            raise ValueError(f"Expected a string but got {type(abstract)} for abstract: {abstract}")

        # 处理单个摘要的tokenization
        inputs = tokenizer(abstract, return_tensors="pt", max_length=512, truncation=True, padding=True)
        inputs = {key: value.to(device) for key, value in inputs.items()}  # 确保inputs在相同设备上
        with torch.no_grad():
            outputs = bert_model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        features.append(cls_embedding.cpu().numpy())  # 将数据移回CPU以便使用NumPy
    return np.vstack(features)


# 加载 BERT 模型用于生成特征
bert_model = BertModel.from_pretrained(tokenizer_path)
bert_model.to(device)  # 将BERT模型移动到设备上
bert_model.eval()

print("Extracting features for incremental data...")
X_incremental = get_bert_embeddings(incremental_abstracts)

# 分类增量数据
predictions = []
with torch.no_grad():
    for i in range(len(X_incremental)):
        inputs = torch.tensor(X_incremental[i]).float().to(device)
        outputs = model(inputs.unsqueeze(0))
        _, predicted = torch.max(outputs, 1)
        predictions.append(predicted.item())

# 将模型预测的标签添加为新列
incremental_df['predicted_label'] = predictions

# 输出分类结果
print("分类完成，结果如下：")
print(incremental_df)

# 保存分类结果到文件，保留原有的列（包括label列）并添加预测标签列
output_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\分类数据\\增量数据\\Biodiversity data journal-before分类结果.xlsx'
incremental_df.to_excel(output_path, index=False, engine='openpyxl')
print(f"分类结果已保存到 {output_path}")
