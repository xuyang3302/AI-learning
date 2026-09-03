import pandas as pd
import matplotlib.pyplot as plt
 
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  

df = pd.read_csv("贵州茅台_600519.csv")

# plt.figure(figsize=(12, 6))          # 画布大小（宽12寸，高6寸）
# plt.plot(df["日期"], df["收盘"], color="red", linewidth=1)
# plt.title("贵州茅台 收盘价走势（2020-2024）")
# plt.xlabel("日期")
# plt.ylabel("收盘价（元）")
# plt.xticks(rotation=45)              # 日期标签旋转45度，防重叠
# plt.xticks(df["日期"][::200])
# plt.tight_layout()                   # 自动调整布局
# plt.show()


# plt.figure(figsize=(12, 4))
# plt.bar(df["日期"], df["成交量"] / 1e4, color="steelblue")  # 除以1e4换成"万股"
# plt.title("贵州茅台 每日成交量")
# plt.ylabel("成交量（万股）")
# plt.xticks(rotation=45)
# plt.xticks(df["日期"][::200])
# plt.tight_layout()
# plt.show()


# plt.figure(figsize=(8, 5))
# plt.hist(df["涨跌幅"], bins=50, color="orange", edgecolor="black")
# plt.title("贵州茅台 每日涨跌幅分布")
# plt.xlabel("涨跌幅（%）")
# plt.ylabel("天数")
# plt.show()


df["MA5"] = df["收盘"].rolling(5).mean()
df["MA20"] = df["收盘"].rolling(20).mean()

plt.figure(figsize=(12, 6))
plt.plot(df["日期"], df["收盘"], color="black", linewidth=1, label="收盘价")
plt.plot(df["日期"], df["MA5"], color="red", linewidth=1, label="MA5")
plt.plot(df["日期"], df["MA20"], color="blue", linewidth=1, label="MA20")
plt.title("贵州茅台：收盘价 + 5日/20日均线")
plt.legend()                          # 显示图例
plt.xticks(df["日期"][::200])
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()