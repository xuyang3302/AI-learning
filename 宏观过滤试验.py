import akshare as ak
import pandas as pd

# 1. 下载上证指数日线
# 指数 = ak.stock_zh_index_daily(symbol="sh000001")
# 指数.to_csv("上证指数.csv", index=False, encoding="utf-8-sig")
# print(指数.head())
# print(f"共 {len(指数)} 行")
# print(指数.columns.tolist())   # 看有哪些列
import akshare as ak
import pandas as pd

# ========== 1. 上证指数：算200日均线，标记牛/熊 ==========
指数 = ak.stock_zh_index_daily(symbol="sh000001")

# 统一日期格式（转成 Pandas 的日期类型，方便后面合并）
指数["date"] = pd.to_datetime(指数["date"])

# 算 200 日均线
指数["MA200"] = 指数["close"].rolling(200).mean()

# 标记牛熊：指数收盘 > MA200 = 牛（1），否则熊（0）
指数["市场"] = 指数["close"] > 指数["MA200"]

# 只要 2020 年之后的数据（和茅台对齐）
指数 = 指数[指数["date"] >= "2020-01-01"]

# ========== 2. 茅台：算均线 + 找金叉（沿用周五代码）==========
茅台 = pd.read_csv("贵州茅台_600519.csv")
茅台["日期"] = pd.to_datetime(茅台["日期"])
茅台["MA5"] = 茅台["收盘"].rolling(5).mean()
茅台["MA20"] = 茅台["收盘"].rolling(20).mean()
茅台["5上穿20"] = 茅台["MA5"] > 茅台["MA20"]
茅台["状态变化"] = 茅台["5上穿20"] != 茅台["5上穿20"].shift(1)
茅台["金叉"] = (茅台["5上穿20"] == True) & (茅台["状态变化"] == True)

# ========== 3. 按日期合并：给每个茅台金叉日标上"那天市场牛/熊" ==========
# 只取指数需要的列，重命名方便合并
指数_简 = 指数[["date", "市场"]].rename(columns={"date": "日期", "市场": "指数牛熊"})

# 左连接：以茅台为主表，把指数牛熊"贴"到对应日期上
茅台 = pd.merge(茅台, 指数_简, on="日期", how="left")

# ========== 4. 分组统计：牛市金叉 vs 熊市金叉 ==========
金叉表 = 茅台[茅台["金叉"]].copy()   # 所有金叉日

牛市金叉 = 金叉表[金叉表["指数牛熊"] == True]
熊市金叉 = 金叉表[金叉表["指数牛熊"] == False]

print(f"牛市金叉：{len(牛市金叉)} 次")
print(f"熊市金叉：{len(熊市金叉)} 次")

# 统计函数：算"金叉后20天涨跌"
def 统计20天(df):
    结果 = []
    for i in df.index:
        if i + 20 < len(茅台):
            当天价 = 茅台.loc[i, "收盘"]
            二十天后 = 茅台.loc[i + 20, "收盘"]
            结果.append((二十天后 - 当天价) / 当天价 * 100)
    return sum(结果) / len(结果) if 结果 else 0

print(f"\n牛市金叉后20天平均：{统计20天(牛市金叉):.2f}%")
print(f"熊市金叉后20天平均：{统计20天(熊市金叉):.2f}%")
print(f"（基准：随机乱买 +0.70%）")