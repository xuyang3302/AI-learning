with open("成绩.csv","r",encoding="utf-8") as f:
    行列表 = f.readlines()
结果行=[]
for 行 in 行列表[1:]:  # 跳过第一行标题
    行 = 行.strip()  # 去掉行首尾的空白字符
    部分 =行.split(",")  # 按逗号拆分
    姓名=部分[0]  # 第一列是姓名
    成绩=部分[1:]  # 剩下的列是成绩
    总分=0
    for 分数 in 成绩:
        总分 += int(分数)  # 累加成绩
    平均分 = 总分 / len(成绩)  # 计算平均分
    结果行.append(f"{姓名},{总分},{平均分:.1f}")  # 格式化输出，保留1位小数

with open("成绩_平均分.csv","w",encoding="utf-8") as f:
    for 结果 in 结果行:
        f.write(结果 + "\n")  # 写入新文件，每行一个结果


for 结果 in 结果行:
    print(结果)  # 打印每个学生的姓名、总分和平均分