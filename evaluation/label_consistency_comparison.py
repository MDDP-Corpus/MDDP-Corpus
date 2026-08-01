# _*_ coding : utf-8 _*_

import pandas as pd

# =========================
# 1. 读取两个 Excel 文件
# =========================

# 修改为你的文件路径
file_a = r"C:\Users\DELL\Desktop\小论文\标识一致性\wos.xlsx"
file_b = r"C:\Users\DELL\Desktop\小论文\标识一致性\scopus.xlsx"

# 读取 Excel
df_a = pd.read_excel(file_a)
df_b = pd.read_excel(file_b)

# =========================
# 2. 提取 DOI 列并统一格式
# =========================

doi_a = (
    df_a["DOI"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
)

doi_b = (
    df_b["DOI"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
)

# 转为集合
set_a = set(doi_a)
set_b = set(doi_b)

# =========================
# 3. 统计相同 DOI 数量
# =========================

same_count = len(set_a.intersection(set_b))

# 输出结果
print(f"a和b中相同的DOI数量为：{same_count}")