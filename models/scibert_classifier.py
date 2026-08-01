import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from transformers import BertTokenizer, BertModel
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

# 指定训练集和测试集的Excel文件路径
train_excel_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\新训练集.xlsx'
test_excel_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\新测试集.xlsx'

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
    def __init__(self):
        super(BERTClassifier, self).__init__()
        self.fc = nn.Linear(768, 2)  # BERT输出的特征向量长度为768，输出维度为2

    def forward(self, x):
        x = self.fc(x)
        return x

# 初始化模型和优化器
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"分类训练将在{'GPU' if torch.cuda.is_available() else 'CPU'}上进行")
model = BERTClassifier().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-5)

# 训练模型
num_epochs = 5
print("开始训练模型...")
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i in tqdm(range(len(X_train)), desc=f"Epoch [{epoch+1}/{num_epochs}]"):
        optimizer.zero_grad()
        inputs = torch.tensor(X_train[i]).float().to(device)
        labels = torch.tensor([y_train[i]]).long().to(device)  # 转换标签为 Long 类型
        outputs = model(inputs.unsqueeze(0))
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    avg_loss = running_loss / len(X_train)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")

# 在测试集上进行预测
print("开始在测试集上验证模型...")
model.eval()
y_pred = []
with torch.no_grad():
    for i in tqdm(range(len(X_test)), desc="Testing"):
        inputs = torch.tensor(X_test[i]).float().to(device)
        outputs = model(inputs.unsqueeze(0))
        _, predicted = torch.max(outputs, 1)
        y_pred.append(predicted.item())

# 计算分类指标
report = classification_report(y_test, y_pred, target_names=["数据论文", "非数据论文"], digits=4, output_dict=True)

# 分别输出数据论文和非数据论文的分类指标
print("数据论文的分类指标：")
print(f"精确率（Precision）：{report['数据论文']['precision']:.4f}")
print(f"召回率（Recall）：{report['数据论文']['recall']:.4f}")
print(f"F1分数（F1-score）：{report['数据论文']['f1-score']:.4f}")
print(f"支持数（Support）：{report['数据论文']['support']}")

print("\n非数据论文的分类指标：")
print(f"精确率（Precision）：{report['非数据论文']['precision']:.4f}")
print(f"召回率（Recall）：{report['非数据论文']['recall']:.4f}")
print(f"F1分数（F1-score）：{report['非数据论文']['f1-score']:.4f}")
print(f"支持数（Support）：{report['非数据论文']['support']}")
