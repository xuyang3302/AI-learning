# A股数据下载器：下载多只股票的历史日线，保存成CSV
import akshare as ak

# 要下载的股票列表（名称, 代码）
股票列表 = [
    ("贵州茅台", "600519"),
    ("五粮液", "000858"),
    ("宁德时代", "300750"),
    ("比亚迪", "002594"),
    ("中天科技", "600522"),   # 你持仓里的！看真实数据
]

for 名称, 代码 in 股票列表:
    print(f"正在下载 {名称}（{代码}）...")
    # 下载历史日线数据（最近5年）
    df = ak.stock_zh_a_hist(symbol=代码, period="daily",
                            start_date="20200101", end_date="20250101")
    # 保存成CSV文件
    df.to_csv(f"{名称}_{代码}.csv", index=False, encoding="utf-8-sig")
    print(f"  ✅ 完成，共 {len(df)} 行数据")

print("全部下载完成！")