# # -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from transformers import BertTokenizer, BertModel, get_scheduler
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import os

# 指定训练集和测试集的Excel文件路径
train_excel_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\训练集.xlsx'
test_excel_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\测试集.xlsx'

# 从训练集和测试集Excel文件中读取数据
train_df = pd.read_excel(train_excel_path, header=None, names=['abstract', 'label'], engine='openpyxl')
test_df = pd.read_excel(test_excel_path, header=None, names=['abstract', 'label'], engine='openpyxl')

# 去除非数值标签并将其转换为整数类型
train_df = train_df[pd.to_numeric(train_df['label'], errors='coerce').notnull()]
test_df = test_df[pd.to_numeric(test_df['label'], errors='coerce').notnull()]
train_df['label'] = train_df['label'].astype(int)
test_df['label'] = test_df['label'].astype(int)

# 提取训练集和测试集的摘要和标签
train_abstracts = train_df['abstract'].tolist()
train_labels = train_df['label'].tolist()
test_abstracts = test_df['abstract'].tolist()
test_labels = test_df['label'].tolist()

# 加载本地的BERT模型和分词器
tokenizer = BertTokenizer.from_pretrained(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\SciBert')
bert_model = BertModel.from_pretrained(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\SciBert')

# 将摘要转换为BERT特征向量
def get_bert_embeddings(abstracts):
    features = []
    for abstract in tqdm(abstracts, desc="Embedding abstracts"):
        inputs = tokenizer(abstract, return_tensors="pt", max_length=512, truncation=True)
        with torch.no_grad():
            outputs = bert_model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        features.append(cls_embedding.numpy())
    return np.vstack(features)

# 获取训练集和测试集的BERT特征向量
print("Extracting features for training set...")
X_train = get_bert_embeddings(train_abstracts)
print("Extracting features for test set...")
X_test = get_bert_embeddings(test_abstracts)

# 将标签转换为数组
y_train = np.array(train_labels)
y_test = np.array(test_labels)

# 定义BERT分类器
class BERTClassifier(nn.Module):
    def __init__(self, dropout_rate=0.3):
        super(BERTClassifier, self).__init__()
        self.dropout = nn.Dropout(p=dropout_rate)
        self.fc = nn.Linear(768, 2)  # BERT输出的特征向量长度为768，输出维度为2

    def forward(self, x):
        x = self.dropout(x)
        x = self.fc(x)
        return x

# 初始化设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"分类训练将在{'GPU' if torch.cuda.is_available() else 'CPU'}上进行")

# 创建模型保存目录
save_dir = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\训练好的模型\\scibert'
os.makedirs(save_dir, exist_ok=True)

# 五折交叉验证
kf = KFold(n_splits=5, shuffle=True, random_state=42)
fold = 1
all_reports = []

# 设置模型参数
num_epochs = 10
learning_rate = 2e-5
batch_size = 16
weight_decay = 0.01

for train_index, val_index in kf.split(X_train):
    print(f"\n----- Fold {fold} -----")
    model = BERTClassifier(dropout_rate=0.3).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    # 添加学习率调度器
    total_steps = num_epochs * len(train_index)
    scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=total_steps)

    # 分割训练集和验证集
    X_fold_train, X_fold_val = X_train[train_index], X_train[val_index]
    y_fold_train, y_fold_val = y_train[train_index], y_train[val_index]

    # 训练模型
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i in tqdm(range(0, len(X_fold_train), batch_size), desc=f"Epoch [{epoch + 1}/{num_epochs}]"):
            inputs = torch.tensor(X_fold_train[i:i + batch_size]).float().to(device)
            labels = torch.tensor(y_fold_train[i:i + batch_size]).long().to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            scheduler.step()
            running_loss += loss.item()

        avg_loss = running_loss / len(X_fold_train)
        print(f"Fold {fold}, Epoch [{epoch + 1}/{num_epochs}], Loss: {avg_loss:.4f}")

    # 保存当前折的模型
    model_save_path = os.path.join(save_dir, f'BERT_model_fold_{fold}.pth')
    torch.save(model.state_dict(), model_save_path)
    print(f"Fold {fold} 的模型已保存到 {model_save_path}")

    # 验证模型
    model.eval()
    y_pred = []
    with torch.no_grad():
        for i in range(len(X_fold_val)):
            inputs = torch.tensor(X_fold_val[i]).float().to(device)
            outputs = model(inputs.unsqueeze(0))
            _, predicted = torch.max(outputs, 1)
            y_pred.append(predicted.item())

    # 计算分类指标
    report = classification_report(
        y_fold_val,
        y_pred,
        labels=[1, 0],  # 1代表“数据论文”，0代表“非数据论文”
        target_names=["数据论文", "非数据论文"],
        digits=4,
        output_dict=True
    )
    all_reports.append(report)

    # 输出当前折的分类指标
    print(f"Fold {fold} 的分类指标：")
    print(f"数据论文的精确率：{report['数据论文']['precision']:.4f}")
    print(f"召回率：{report['数据论文']['recall']:.4f}")
    print(f"F1分数：{report['数据论文']['f1-score']:.4f}")
    print(f"非数据论文的精确率：{report['非数据论文']['precision']:.4f}")
    print(f"召回率：{report['非数据论文']['recall']:.4f}")
    print(f"F1分数：{report['非数据论文']['f1-score']:.4f}")
    print(f"支持数（support）：{report['数据论文']['support']} (数据论文), {report['非数据论文']['support']} (非数据论文)")

    fold += 1

# 在所有折叠上汇总分类指标
print("\n所有折叠的平均分类指标：")
average_report = {key: {metric: np.mean([report[key][metric] for report in all_reports]) for metric in
                        ['precision', 'recall', 'f1-score', 'support']} for key in ["数据论文", "非数据论文"]}
for label in average_report:
    print(f"{label} 的分类指标：")
    print(f"精确率：{average_report[label]['precision']:.4f}")
    print(f"召回率：{average_report[label]['recall']:.4f}")
    print(f"F1分数：{average_report[label]['f1-score']:.4f}")
    print(f"支持数（support）：{average_report[label]['support']:.0f}")