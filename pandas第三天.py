import pandas as pd

df = pd.read_csv("贵州茅台_600519.csv")

# print("===每列缺失数量===")
# # print(df.isnull().sum())
df["MA5"] = df["收盘"].rolling(5).mean()    # 5日均线
df["MA20"] = df["收盘"].rolling(20).mean()  # 20日均线

# # === 看结果 ===
# print(df[["日期", "收盘", "MA5", "MA20"]].head(10))
茅台 = pd.read_csv("贵州茅台_600519.csv")
五粮液 = pd.read_csv("五粮液_000858.csv")

# 各自加一列股票名，方便区分
# 茅台["股票"] = "茅台"
# 五粮液["股票"] = "五粮液"

# # === 纵向合并（上下拼接）===
# 全部 = pd.concat([茅台, 五粮液], ignore_index=True)
# print("=== 合并后 ===")
# print(全部[["日期", "股票", "收盘"]].tail(5))
# print(f"总行数：{len(全部)}（茅台{len(茅台)} + 五粮液{len(五粮液)}）")

df["5上穿20"] = df["MA5"] > df["MA20"]     # True=MA5在上，False=在下

# 找"从False变True"的日子 = 金叉发生日
df["状态变化"] = df["5上穿20"] != df["5上穿20"].shift(1)   # 和昨天比，变了吗
df["金叉"] = (df["5上穿20"] == True) & (df["状态变化"] == True)

print("=== 金叉发生日（前10次）===")
print(df[df["金叉"]][["日期", "收盘", "MA5", "MA20"]].head(10))