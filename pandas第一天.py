import pandas as pd

df = pd.read_csv('贵州茅台_600519.csv')  # Replace 'data.csv' with your actual file path

print("=== 前5行 ===")
print(df.head())

print("\n=== 数据概况 ===")
print(df.info())       # 每列的类型、有多少非空值
print("\n=== 统计摘要 ===")
print(df.describe())   # 每列的 均值/最大/最小/分位数

# ③ 选列 —— 按列名取
print("\n=== 收盘价前5个 ===")
print(df["收盘"].head())     # 取"收盘"这一列