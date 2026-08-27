try:
    # 文件 = open("不存在的文件.csv", "r", encoding="utf-8")
    # 内容 = 文件.read()
    # 价格 = "茅台"
    # print(价格 + 100)
    # print(成本价)   # 变量名拼错/没定义
    列表 = [1, 2, 3]
    print(列表[5])
except FileNotFoundError:
    print("文件不存在！请检查文件名。")
except Exception as 错误:
    print(f"出错了：{错误}")