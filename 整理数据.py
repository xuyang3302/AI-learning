import csv 

def 加涨跌幅(文件名):
    with open(文件名, 'r', encoding='utf-8-sig') as 文件:
        reader = csv.reader(文件)
        行列表 = list(reader)
        表头 = 行列表[0]+["涨跌幅"]
        新行列表 = [表头]

    for i in range(1, len(行列表)):
        今天 = 行列表[i]
        if i == 1:                     # 第一条数据没有昨天，涨跌幅留空
            新行列表.append(今天 + [""])
            continue
        昨天 = 行列表[i - 1]             # 上一行 = 昨天的数据
        今收 = float(今天[3])            # 收盘价在第3列（索引3）
        昨收 = float(昨天[3])
        涨跌幅 = (今收 - 昨收) / 昨收 * 100
        新行列表.append(今天 + [f"{涨跌幅:.2f}"])

    新文件名 = 文件名.replace(".csv", "_整理.csv")
    with open(新文件名, "w", encoding="utf-8-sig", newline="") as 文件:
        csv.writer(文件).writerows(新行列表)

股票文件 = [
    "贵州茅台_600519.csv",
    "五粮液_000858.csv",
    "宁德时代_300750.csv",
    "比亚迪_002594.csv",
    "中天科技_600522.csv",
]

for 文件名 in 股票文件:
    加涨跌幅(文件名)