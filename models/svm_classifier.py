# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)
#
# import pandas as pd
# import re
# from collections import Counter
# from gensim.models import Doc2Vec
# from gensim.models.doc2vec import TaggedDocument
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import SVC
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
# from tqdm import tqdm
# import numpy as np
#
# # 使用 openpyxl 处理 .xlsx 文件
# print("正在加载数据集...")
# train_data = pd.read_excel(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\不平衡处理\\训练集.xlsx', engine='openpyxl')
# validation_data = pd.read_excel(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\不平衡处理\\完整数据集.xlsx', engine='openpyxl')
#
# # 打印列名，检查是否包含'label'
# print("训练集列名：", train_data.columns)
# print("验证集列名：", validation_data.columns)
#
# # 确保摘要列为字符串类型
# print("正在处理数据类型...")
# train_data['摘要'] = train_data['摘要'].astype(str)
# validation_data['摘要'] = validation_data['摘要'].astype(str)
#
# # 清洗文本数据
# def clean_text(text):
#     if not isinstance(text, str):
#         raise TypeError(f"Expected a string, got {type(text)} instead")
#     text = re.sub(r'\W+', ' ', text)
#     text = text.lower()
#     return text
#
# # 添加进度条到数据清洗步骤
# print("正在清洗文本数据...")
# tqdm.pandas(desc="Cleaning text")
# train_data['cleaned_abstract'] = train_data['摘要'].progress_apply(clean_text)
# validation_data['cleaned_abstract'] = validation_data['摘要'].progress_apply(clean_text)
#
# # 检查数据中是否包含'label'列
# if 'label' not in train_data.columns:
#     raise KeyError("训练集中缺少'label'列")
#
# # 分离数据论文和非数据论文的摘要
# print("正在分离数据论文和非数据论文...")
# data_papers = train_data[train_data['label'] == 1]
# non_data_papers = train_data[train_data['label'] == 0]
#
# # 统计高频词
# print("正在统计高频词...")
# def get_high_freq_words(texts, n=100):
#     all_words = ' '.join(texts).split()
#     freq_dist = Counter(all_words)
#     common_words = [word for word, _ in freq_dist.most_common(n)]
#     return set(common_words)
#
# # 获取并保存完整的高频词
# data_freq_words = get_high_freq_words(data_papers['cleaned_abstract'])
# non_data_freq_words = get_high_freq_words(non_data_papers['cleaned_abstract'])
#
# # 保存完整的高频词到文件
# print("正在保存完整高频词...")
# with open(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\不平衡处理\\data_freq_words.txt', 'w') as f:
#     for word in data_freq_words:
#         f.write(word + '\n')
#
# with open(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\不平衡处理\\non_data_freq_words.txt', 'w') as f:
#     for word in non_data_freq_words:
#         f.write(word + '\n')
#
# # 获取独特的高频词
# print("正在获取独特高频词...")
# unique_data_freq_words = data_freq_words - non_data_freq_words
# unique_non_data_freq_words = non_data_freq_words - data_freq_words
#
# # 将独特的高频词保存到文件
# print("正在保存独特高频词...")
# with open(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\不平衡处理\\unique_data_freq_words.txt', 'w') as f:
#     for word in unique_data_freq_words:
#         f.write(word + '\n')
#
# with open(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\不平衡处理\\unique_non_data_freq_words.txt', 'w') as f:
#     for word in unique_non_data_freq_words:
#         f.write(word + '\n')
#
# # 使用TF-IDF向量表示高频词
# print("正在使用TF-IDF表示高频词...")
# tfidf_vectorizer = TfidfVectorizer(vocabulary=unique_data_freq_words | unique_non_data_freq_words)
# tfidf_features = tfidf_vectorizer.fit_transform(train_data['cleaned_abstract'])
# validation_tfidf_features = tfidf_vectorizer.transform(validation_data['cleaned_abstract'])
#
# # Doc2Vec模型训练（使用DBOW模型）
# print("正在训练Doc2Vec模型...")
# tagged_docs = [TaggedDocument(words=doc.split(), tags=[i]) for i, doc in enumerate(train_data['cleaned_abstract'])]
# doc2vec_model = Doc2Vec(tagged_docs, vector_size=100, window=5, min_count=2, workers=4, dm=0)
#
# # 生成Doc2Vec特征
# def get_doc2vec_features(model, texts):
#     return [model.infer_vector(text.split()) for text in texts]
#
# print("正在生成Doc2Vec特征...")
# train_data['doc2vec_feature'] = get_doc2vec_features(doc2vec_model, train_data['cleaned_abstract'])
# validation_data['doc2vec_feature'] = get_doc2vec_features(doc2vec_model, validation_data['cleaned_abstract'])
#
# # 分批合并所有特征
# def combine_features(data, tfidf_features, batch_size=300):
#     num_batches = int(np.ceil(len(data) / batch_size))
#     features = []
#     for batch in tqdm(range(num_batches), desc="Combining features in batches"):
#         start = batch * batch_size
#         end = min((batch + 1) * batch_size, len(data))
#         batch_features = []
#         for i in range(start, end):
#             doc2vec_feature = data.iloc[i]['doc2vec_feature']
#             tfidf_feature = tfidf_features[i].toarray()[0]
#             combined_feature = list(doc2vec_feature) + list(tfidf_feature)
#             batch_features.append(combined_feature)
#         features.extend(batch_features)
#     return pd.DataFrame(features)
#
# # 添加进度条到合并特征步骤
# print("正在合并特征...")
# train_features_df = combine_features(train_data, tfidf_features)
# validation_features_df = combine_features(validation_data, validation_tfidf_features)
#
# # 训练SVM模型
# print("正在训练SVM模型...")
# svm_model = make_pipeline(StandardScaler(), SVC(class_weight='balanced'))
# svm_model.fit(train_features_df, train_data['label'])
#
# # 在验证集上进行预测并输出性能
# print("正在验证集上进行预测...")
# y_val_pred = svm_model.predict(validation_features_df)
#
# # 使用 classification_report 的输出保留四位小数
# print("验证集分类报告：")
# print(classification_report(validation_data['label'], y_val_pred, digits=4))
#
# # 精确率、召回率、F1-score保留四位小数
# precision = precision_score(validation_data['label'], y_val_pred, average='macro')
# recall = recall_score(validation_data['label'], y_val_pred, average='macro')
# f1 = f1_score(validation_data['label'], y_val_pred, average='macro')
#
# print(f"验证集精确率: {precision:.4f}")
# print(f"验证集召回率: {recall:.4f}")
# print(f"验证集F1-score: {f1:.4f}")
#
# # 将预测结果添加到验证集数据框
# print("正在保存预测结果...")
# validation_data['predicted_label'] = y_val_pred
#
# # 将验证集数据框保存到Excel文件
# print("正在保存验证集数据框...")
# validation_data.to_excel('D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\不平衡_test_predictions1.xlsx', index=False, engine='openpyxl')
#
# print("所有步骤完成！")




# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)
#
# import pandas as pd
# import re
# from collections import Counter
# from gensim.models import Word2Vec
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import SVC
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
# from tqdm import tqdm
# import numpy as np
#
# # 使用 openpyxl 处理 .xlsx 文件
# print("正在加载数据集...")
# train_data = pd.read_excel(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\不平衡处理\\训练集.xlsx', engine='openpyxl')
# validation_data = pd.read_excel(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\不平衡处理\\完整数据集.xlsx', engine='openpyxl')
#
# # 打印列名，检查是否包含'label'
# print("训练集列名：", train_data.columns)
# print("验证集列名：", validation_data.columns)
#
# # 确保摘要列为字符串类型
# print("正在处理数据类型...")
# train_data['摘要'] = train_data['摘要'].astype(str)
# validation_data['摘要'] = validation_data['摘要'].astype(str)
#
# # 清洗文本数据
# def clean_text(text):
#     if not isinstance(text, str):
#         raise TypeError(f"Expected a string, got {type(text)} instead")
#     text = re.sub(r'\W+', ' ', text)
#     text = text.lower()
#     return text
#
# # 添加进度条到数据清洗步骤
# print("正在清洗文本数据...")
# tqdm.pandas(desc="Cleaning text")
# train_data['cleaned_abstract'] = train_data['摘要'].progress_apply(clean_text)
# validation_data['cleaned_abstract'] = validation_data['摘要'].progress_apply(clean_text)
#
# # 检查数据中是否包含'label'列
# if 'label' not in train_data.columns:
#     raise KeyError("训练集中缺少'label'列")
#
# # 分离数据论文和非数据论文的摘要
# print("正在分离数据论文和非数据论文...")
# data_papers = train_data[train_data['label'] == 1]
# non_data_papers = train_data[train_data['label'] == 0]
#
# # 统计高频词
# print("正在统计高频词...")
# def get_high_freq_words(texts, n=100):
#     all_words = ' '.join(texts).split()
#     freq_dist = Counter(all_words)
#     common_words = [word for word, _ in freq_dist.most_common(n)]
#     return set(common_words)
#
# # 获取并保存完整的高频词
# data_freq_words = get_high_freq_words(data_papers['cleaned_abstract'])
# non_data_freq_words = get_high_freq_words(non_data_papers['cleaned_abstract'])
#
# # 保存完整的高频词到文件
# print("正在保存完整高频词...")
# with open(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\data_freq_words.txt', 'w') as f:
#     for word in data_freq_words:
#         f.write(word + '\n')
#
# with open(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\non_data_freq_words.txt', 'w') as f:
#     for word in non_data_freq_words:
#         f.write(word + '\n')
#
# # 获取独特的高频词
# print("正在获取独特高频词...")
# unique_data_freq_words = data_freq_words - non_data_freq_words
# unique_non_data_freq_words = non_data_freq_words - data_freq_words
#
# # 将独特的高频词保存到文件
# print("正在保存独特高频词...")
# with open(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\unique_data_freq_words.txt', 'w') as f:
#     for word in unique_data_freq_words:
#         f.write(word + '\n')
#
# with open(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\unique_non_data_freq_words.txt', 'w') as f:
#     for word in unique_non_data_freq_words:
#         f.write(word + '\n')
#
# # 使用TF-IDF向量表示高频词
# print("正在使用TF-IDF表示高频词...")
# tfidf_vectorizer = TfidfVectorizer(vocabulary=unique_data_freq_words | unique_non_data_freq_words)
# tfidf_features = tfidf_vectorizer.fit_transform(train_data['cleaned_abstract'])
# validation_tfidf_features = tfidf_vectorizer.transform(validation_data['cleaned_abstract'])
#
# # Word2Vec模型训练
# print("正在训练Word2Vec模型...")
# sentences = [doc.split() for doc in train_data['cleaned_abstract']]
# word2vec_model = Word2Vec(sentences, vector_size=100, window=5, min_count=2, workers=4)
#
# # 生成Word2Vec特征
# def get_word2vec_features(model, texts):
#     features = []
#     for text in texts:
#         words = text.split()
#         word_vectors = [model.wv[word] for word in words if word in model.wv]
#         if len(word_vectors) > 0:
#             sentence_vector = np.mean(word_vectors, axis=0)  # 平均化词向量
#         else:
#             sentence_vector = np.zeros(model.vector_size)  # 如果没有词向量，返回全零向量
#         features.append(sentence_vector)
#     return features
#
# print("正在生成Word2Vec特征...")
# train_data['word2vec_feature'] = get_word2vec_features(word2vec_model, train_data['cleaned_abstract'])
# validation_data['word2vec_feature'] = get_word2vec_features(word2vec_model, validation_data['cleaned_abstract'])

# 分批合并所有特征
# def combine_features(data, tfidf_features, batch_size=300):
#     num_batches = int(np.ceil(len(data) / batch_size))
#     features = []
#     for batch in tqdm(range(num_batches), desc="Combining features in batches"):
#         start = batch * batch_size
#         end = min((batch + 1) * batch_size, len(data))
#         batch_features = []
#         for i in range(start, end):
#             word2vec_feature = data.iloc[i]['word2vec_feature']
#             tfidf_feature = tfidf_features[i].toarray()[0]
#             combined_feature = list(word2vec_feature) + list(tfidf_feature)
#             batch_features.append(combined_feature)
#         features.extend(batch_features)
#     return pd.DataFrame(features)
#
# # 添加进度条到合并特征步骤
# print("正在合并特征...")
# train_features_df = combine_features(train_data, tfidf_features)
# validation_features_df = combine_features(validation_data, validation_tfidf_features)
#
# # 训练SVM模型
# print("正在训练SVM模型...")
# svm_model = make_pipeline(StandardScaler(), SVC(class_weight='balanced'))
# svm_model.fit(train_features_df, train_data['label'])
#
# # 在验证集上进行预测并输出性能
# print("正在验证集上进行预测...")
# y_val_pred = svm_model.predict(validation_features_df)
#
# # 使用 classification_report 的输出保留四位小数
# print("验证集分类报告：")
# print(classification_report(validation_data['label'], y_val_pred, digits=4))
#
# # 精确率、召回率、F1-score保留四位小数
# precision = precision_score(validation_data['label'], y_val_pred, average='macro')
# recall = recall_score(validation_data['label'], y_val_pred, average='macro')
# f1 = f1_score(validation_data['label'], y_val_pred, average='macro')
#
# print(f"验证集精确率: {precision:.4f}")
# print(f"验证集召回率: {recall:.4f}")
# print(f"验证集F1-score: {f1:.4f}")
#
# # 将预测结果添加到验证集数据框
# print("正在保存预测结果...")
# validation_data['predicted_label'] = y_val_pred
#
# # 将验证集数据框保存到Excel文件
# print("正在保存验证集数据框...")
# validation_data.to_excel('D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\不平衡_test_predictions2.xlsx', index=False, engine='openpyxl')
#
# print("所有步骤完成！")

#五折交叉验证代码
# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)
#
# import pandas as pd
# import re
# from collections import Counter
# from gensim.models import Word2Vec
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import SVC
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
# from sklearn.model_selection import KFold
# from tqdm import tqdm
# import numpy as np
#
# # 使用 openpyxl 处理 .xlsx 文件
# print("正在加载数据集...")
# train_data = pd.read_excel(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\新训练集.xlsx', engine='openpyxl')
# validation_data = pd.read_excel(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\新测试集.xlsx', engine='openpyxl')
#
# # 将训练集和测试集合并为一个完整数据集
# print("正在合并训练集和测试集...")
# full_data = pd.concat([train_data, validation_data], ignore_index=True)
#
# # 打印列名，检查是否包含'label'
# print("数据集列名：", full_data.columns)
#
# # 确保摘要列为字符串类型
# print("正在处理数据类型...")
# full_data['摘要'] = full_data['摘要'].astype(str)
#
# # 清洗文本数据
# def clean_text(text):
#     if not isinstance(text, str):
#         raise TypeError(f"Expected a string, got {type(text)} instead")
#     text = re.sub(r'\W+', ' ', text)
#     text = text.lower()
#     return text
#
# # 添加进度条到数据清洗步骤
# print("正在清洗文本数据...")
# tqdm.pandas(desc="Cleaning text")
# full_data['cleaned_abstract'] = full_data['摘要'].progress_apply(clean_text)
#
# # 检查数据中是否包含'label'列
# if 'label' not in full_data.columns:
#     raise KeyError("数据集中缺少'label'列")
#
# # 分离数据论文和非数据论文的摘要
# print("正在分离数据论文和非数据论文...")
# data_papers = full_data[full_data['label'] == 1]
# non_data_papers = full_data[full_data['label'] == 0]
#
# # 统计高频词
# print("正在统计高频词...")
# def get_high_freq_words(texts, n=100):
#     all_words = ' '.join(texts).split()
#     freq_dist = Counter(all_words)
#     common_words = [word for word, _ in freq_dist.most_common(n)]
#     return set(common_words)
#
# # 获取并保存完整的高频词
# data_freq_words = get_high_freq_words(data_papers['cleaned_abstract'])
# non_data_freq_words = get_high_freq_words(non_data_papers['cleaned_abstract'])
#
# # 使用TF-IDF向量表示高频词
# print("正在使用TF-IDF表示高频词...")
# tfidf_vectorizer = TfidfVectorizer(vocabulary=data_freq_words | non_data_freq_words)
# tfidf_features = tfidf_vectorizer.fit_transform(full_data['cleaned_abstract'])
#
# # Word2Vec模型训练
# print("正在训练Word2Vec模型...")
# sentences = [doc.split() for doc in full_data['cleaned_abstract']]
# word2vec_model = Word2Vec(sentences, vector_size=100, window=5, min_count=2, workers=4)
#
# # 生成Word2Vec特征
# def get_word2vec_features(model, texts):
#     features = []
#     for text in texts:
#         words = text.split()
#         word_vectors = [model.wv[word] for word in words if word in model.wv]
#         if len(word_vectors) > 0:
#             sentence_vector = np.mean(word_vectors, axis=0)  # 平均化词向量
#         else:
#             sentence_vector = np.zeros(model.vector_size)  # 如果没有词向量，返回全零向量
#         features.append(sentence_vector)
#     return features
#
# print("正在生成Word2Vec特征...")
# full_data['word2vec_feature'] = get_word2vec_features(word2vec_model, full_data['cleaned_abstract'])
#
# # 分批合并所有特征
# def combine_features(data, tfidf_features, batch_size=300):
#     num_batches = int(np.ceil(len(data) / batch_size))
#     features = []
#     for batch in tqdm(range(num_batches), desc="Combining features in batches"):
#         start = batch * batch_size
#         end = min((batch + 1) * batch_size, len(data))
#         batch_features = []
#         for i in range(start, end):
#             word2vec_feature = data.iloc[i]['word2vec_feature']
#             tfidf_feature = tfidf_features[i].toarray()[0]
#             combined_feature = list(word2vec_feature) + list(tfidf_feature)
#             batch_features.append(combined_feature)
#         features.extend(batch_features)
#     return pd.DataFrame(features)
#
# # 添加进度条到合并特征步骤
# print("正在合并特征...")
# full_features_df = combine_features(full_data, tfidf_features)
#
# # 创建五折交叉验证对象
# kf = KFold(n_splits=5, shuffle=True, random_state=42)
#
# # 初始化SVM模型
# svm_model = make_pipeline(StandardScaler(), SVC(class_weight='balanced'))
#
# # 用于保存每一折的分数
# precision_scores = []
# recall_scores = []
# f1_scores = []
#
# # 开始五折交叉验证
# print("正在进行五折交叉验证...")
#
# for fold, (train_index, val_index) in enumerate(kf.split(full_features_df), 1):
#     # 划分训练集和验证集
#     X_train, X_val = full_features_df.iloc[train_index], full_features_df.iloc[val_index]
#     y_train, y_val = full_data['label'].iloc[train_index], full_data['label'].iloc[val_index]
#
#     # 训练SVM模型
#     svm_model.fit(X_train, y_train)
#
#     # 在验证集上进行预测
#     y_val_pred = svm_model.predict(X_val)
#
#     # 计算当前折的precision, recall, f1 score
#     precision = precision_score(y_val, y_val_pred, average='macro')
#     recall = recall_score(y_val, y_val_pred, average='macro')
#     f1 = f1_score(y_val, y_val_pred, average='macro')
#
#     # 保存分数
#     precision_scores.append(precision)
#     recall_scores.append(recall)
#     f1_scores.append(f1)
#
#     # 输出当前折的分类指标
#     print(f"第 {fold} 折的分类指标：")
#     print(f"精确率: {precision:.4f}, 召回率: {recall:.4f}, F1-score: {f1:.4f}")
#     print(classification_report(y_val, y_val_pred, digits=4))
#
# # 输出每折的平均结果
# print(f"五折交叉验证的平均精确率: {np.mean(precision_scores):.4f}")
# print(f"五折交叉验证的平均召回率: {np.mean(recall_scores):.4f}")
# print(f"五折交叉验证的平均F1-score: {np.mean(f1_scores):.4f}")
#
# print("所有步骤完成！")
# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)
#
# import pandas as pd
# import re
# from collections import Counter
# from gensim.models import Doc2Vec
# from gensim.models.doc2vec import TaggedDocument
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import SVC
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
# from sklearn.model_selection import KFold
# from tqdm import tqdm
# import numpy as np
#
# # 使用 openpyxl 处理 .xlsx 文件
# print("正在加载数据集...")
# train_data = pd.read_excel(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\新训练集.xlsx', engine='openpyxl')
# validation_data = pd.read_excel(r'D:\\ftp\\LIUyt\\文本分类bert\\niutong\\机器学习分类\\数据集\\新测试集.xlsx', engine='openpyxl')
#
# # 将训练集和测试集合并为一个完整数据集
# print("正在合并训练集和测试集...")
# full_data = pd.concat([train_data, validation_data], ignore_index=True)
#
# # 打印列名，检查是否包含'label'
# print("数据集列名：", full_data.columns)
#
# # 确保摘要列为字符串类型
# print("正在处理数据类型...")
# full_data['摘要'] = full_data['摘要'].astype(str)
#
# # 清洗文本数据
# def clean_text(text):
#     if not isinstance(text, str):
#         raise TypeError(f"Expected a string, got {type(text)} instead")
#     text = re.sub(r'\W+', ' ', text)
#     text = text.lower()
#     return text
#
# # 添加进度条到数据清洗步骤
# print("正在清洗文本数据...")
# tqdm.pandas(desc="Cleaning text")
# full_data['cleaned_abstract'] = full_data['摘要'].progress_apply(clean_text)
#
# # 检查数据中是否包含'label'列
# if 'label' not in full_data.columns:
#     raise KeyError("数据集中缺少'label'列")
#
# # 分离数据论文和非数据论文的摘要
# print("正在分离数据论文和非数据论文...")
# data_papers = full_data[full_data['label'] == 1]
# non_data_papers = full_data[full_data['label'] == 0]
#
# # 统计高频词
# print("正在统计高频词...")
# def get_high_freq_words(texts, n=100):
#     all_words = ' '.join(texts).split()
#     freq_dist = Counter(all_words)
#     common_words = [word for word, _ in freq_dist.most_common(n)]
#     return set(common_words)
#
# # 获取并保存完整的高频词
# data_freq_words = get_high_freq_words(data_papers['cleaned_abstract'])
# non_data_freq_words = get_high_freq_words(non_data_papers['cleaned_abstract'])
#
# # 使用TF-IDF向量表示高频词
# print("正在使用TF-IDF表示高频词...")
# tfidf_vectorizer = TfidfVectorizer(vocabulary=data_freq_words | non_data_freq_words)
# tfidf_features = tfidf_vectorizer.fit_transform(full_data['cleaned_abstract'])
#
# # Doc2Vec模型训练
# print("正在训练Doc2Vec模型...")
# tagged_docs = [TaggedDocument(words=doc.split(), tags=[i]) for i, doc in enumerate(full_data['cleaned_abstract'])]
# doc2vec_model = Doc2Vec(tagged_docs, vector_size=100, window=5, min_count=2, workers=4)
#
# # 生成Doc2Vec特征
# def get_doc2vec_features(model, texts):
#     features = []
#     for i, text in enumerate(texts):
#         doc_vector = model.dv[i]  # 获取文档向量
#         features.append(doc_vector)
#     return features
#
# print("正在生成Doc2Vec特征...")
# full_data['doc2vec_feature'] = get_doc2vec_features(doc2vec_model, full_data['cleaned_abstract'])
#
# # 分批合并所有特征
# def combine_features(data, tfidf_features, batch_size=300):
#     num_batches = int(np.ceil(len(data) / batch_size))
#     features = []
#     for batch in tqdm(range(num_batches), desc="Combining features in batches"):
#         start = batch * batch_size
#         end = min((batch + 1) * batch_size, len(data))
#         batch_features = []
#         for i in range(start, end):
#             doc2vec_feature = data.iloc[i]['doc2vec_feature']
#             tfidf_feature = tfidf_features[i].toarray()[0]
#             combined_feature = list(doc2vec_feature) + list(tfidf_feature)
#             batch_features.append(combined_feature)
#         features.extend(batch_features)
#     return pd.DataFrame(features)
#
# # 添加进度条到合并特征步骤
# print("正在合并特征...")
# full_features_df = combine_features(full_data, tfidf_features)
#
# # 创建五折交叉验证对象
# kf = KFold(n_splits=5, shuffle=True, random_state=42)
#
# # 初始化SVM模型
# svm_model = make_pipeline(StandardScaler(), SVC(class_weight='balanced'))
#
# # 用于保存每一折的分数
# precision_scores = []
# recall_scores = []
# f1_scores = []
#
# # 开始五折交叉验证
# print("正在进行五折交叉验证...")
#
# for fold, (train_index, val_index) in enumerate(kf.split(full_features_df), 1):
#     # 划分训练集和验证集
#     X_train, X_val = full_features_df.iloc[train_index], full_features_df.iloc[val_index]
#     y_train, y_val = full_data['label'].iloc[train_index], full_data['label'].iloc[val_index]
#
#     # 训练SVM模型
#     svm_model.fit(X_train, y_train)
#
#     # 在验证集上进行预测
#     y_val_pred = svm_model.predict(X_val)
#
#     # 计算当前折的precision, recall, f1 score
#     precision = precision_score(y_val, y_val_pred, average='macro')
#     recall = recall_score(y_val, y_val_pred, average='macro')
#     f1 = f1_score(y_val, y_val_pred, average='macro')
#
#     # 保存分数
#     precision_scores.append(precision)
#     recall_scores.append(recall)
#     f1_scores.append(f1)
#
#     # 输出当前折的分类指标
#     print(f"第 {fold} 折的分类指标：")
#     print(f"精确率: {precision:.4f}, 召回率: {recall:.4f}, F1-score: {f1:.4f}")
#     print(classification_report(y_val, y_val_pred, digits=4))
#
# # 输出每折的平均结果
# print(f"五折交叉验证的平均精确率: {np.mean(precision_scores):.4f}")
# print(f"五折交叉验证的平均召回率: {np.mean(recall_scores):.4f}")
# print(f"五折交叉验证的平均F1-score: {np.mean(f1_scores):.4f}")
#
# print("所有步骤完成！")
