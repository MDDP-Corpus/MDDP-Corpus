import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

# 1. 从指定位置导入 Excel 文件
file_path = r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\分类数据\\增量数据\\scientific data-after分类结果.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path, engine='openpyxl')

# 检查列名是否正确
print(df.columns)

# 2. 提取真实标签和模型输出标签
true_labels = df['文章类型']  # 真实标签
predicted_labels = df['predicted_label']  # 模型分类后的标签

# 3. 计算性能指标
# precision = precision_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels)
recall = recall_score(true_labels, predicted_labels)
f1 = f1_score(true_labels, predicted_labels)

# 输出结果
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# 输出完整的分类报告
print("\nClassification Report:")
print(classification_report(true_labels, predicted_labels, digits=4))

