# -*- coding: utf-8 -*-
"""
DeepSeek 命令行对话程序 —— 第 1 周周三任务模板
=================================================
用途：在终端里和 DeepSeek 对话（多轮、可存档、支持系统提示词、支持 JSON 输出）。
第 11 周做财报问答时，你还会复用这里的 API 调用模式。

【使用前必做】
1. 设置 API Key（两种方式任选）：
   - 方式 A（推荐）：终端执行
        set DEEPSEEK_API_KEY=sk-你的key        （cmd）
        $env:DEEPSEEK_API_KEY="sk-你的key"     （PowerShell）
   - 方式 B：把下面 get_api_key() 里的注释打开，直接填你的 key（仅本地测试用）
2. 安装依赖：pip install requests
3. 运行：python chat_cli.py

【内置命令】（对话中直接输入）
  /exit        退出程序
  /save        把当前对话保存到 chat_history.md
  /system 内容  切换系统提示词（周五 Prompt 实验用）
  /clear       清空当前对话历史
  /json 内容    让 AI 以 JSON 格式回答（周五实验用）

【学习提示】周三的任务是"逐行读懂再运行"：
  每段代码上方的注释解释"这段在干什么"，读完再往下看。
  读完后试着回答：去掉哪一行程序会坏？为什么？
"""

import json      # 用来把 Python 对象转成 JSON 字符串 / 解析 JSON
import os        # 用来读取环境变量（你的 API Key 存在这里，不写进代码）
import sys       # 用来处理退出
import requests  # 用来向 DeepSeek 服务器发 HTTP 请求

# DeepSeek 的接口地址（OpenAI 兼容格式）和模型名
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"


def get_api_key():
    """从环境变量读取 API Key。找不到就提示并退出。"""
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        # 方式 B（不推荐，仅本地测试）：直接写死在这里
        # key = "sk-你的key"
        print("错误：没有找到 API Key。")
        print("请先设置环境变量 DEEPSEEK_API_KEY，或在代码里按注释填写。")
        sys.exit(1)
    return key


def call_deepseek(messages):
    """
    向 DeepSeek 发一次请求，返回 AI 的回复文本。

    参数 messages 是一个列表，元素是 {"role": "...", "content": "..."}：
      - role 有三种：system（系统提示词）、user（你）、assistant（AI）
      - 把整个历史都发给服务器，AI 才能"记住"前面的对话（多轮对话的原理）
    """
    headers = {
        "Authorization": f"Bearer {get_api_key()}",  # 鉴权头，携带你的 Key
        "Content-Type": "application/json",          # 告诉服务器发送的是 JSON
    }
    payload = {
        "model": MODEL,        # 用哪个模型
        "messages": messages,  # 对话历史
        "stream": False,       # 关闭流式输出（简单起见）
    }
    # 发 POST 请求；timeout=60 表示最多等 60 秒，防止卡死
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        # 非 200 说明出错：把服务器返回的错误信息打印出来，方便排查
        print(f"请求失败（HTTP {resp.status_code}）：{resp.text}")
        return None
    data = resp.json()  # 把返回的 JSON 文本解析成 Python 字典
    # 返回结构：choices[0].message.content 就是 AI 的回复文本
    return data["choices"][0]["message"]["content"]


def save_history(messages):
    """把对话历史保存成 Markdown 文件，方便回看和复盘。"""
    if not messages:
        print("当前没有对话内容，跳过保存。")
        return
    lines = ["# 对话记录\n"]
    for msg in messages:
        role_name = {"system": "【系统】", "user": "【你】", "assistant": "【AI】"}.get(
            msg["role"], msg["role"]
        )
        lines.append(f"{role_name}\n\n{msg['content']}\n")
    with open("chat_history.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("已保存到 chat_history.md")


def main():
    """主程序：循环等待输入 → 调 API → 打印回复。"""
    print("=" * 50)
    print("DeepSeek 命令行对话程序已启动")
    print("输入内容开始对话；输入 /help 查看命令；输入 /exit 退出")
    print("=" * 50)

    # 对话历史：第一条是系统提示词（给 AI 设定角色/规则）
    messages = [{"role": "system", "content": "你是一个乐于助人的 AI 助手。"}]

    while True:
        try:
            user_input = input("\n你> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n再见！")
            break

        if not user_input:
            continue

        # ---------- 处理内置命令 ----------
        if user_input == "/exit":
            print("再见！")
            break
        elif user_input == "/save":
            save_history(messages)
            continue
        elif user_input == "/clear":
            messages = [messages[0]]  # 只保留系统提示词
            print("已清空对话历史。")
            continue
        elif user_input.startswith("/system"):
            # /system 新提示词 → 替换系统提示词（周五 Prompt 实验用）
            new_system = user_input[len("/system"):].strip()
            if new_system:
                messages[0] = {"role": "system", "content": new_system}
                print(f"系统提示词已更新为：{new_system}")
            else:
                print("用法：/system 新的提示词内容")
            continue
        elif user_input.startswith("/json"):
            # /json 内容 → 强制要求 AI 输出 JSON（周五实验用）
            task = user_input[len("/json"):].strip()
            messages.append(
                {"role": "user", "content": f"{task}\n请只输出 JSON，不要任何其他文字。"}
            )
        elif user_input == "/help":
            print("命令列表：/exit 退出 | /save 保存 | /clear 清空 | "
                  "/system 内容 换提示词 | /json 内容 要求JSON输出")
            continue
        else:
            messages.append({"role": "user", "content": user_input})

        # ---------- 调用 API ----------
        print("\nAI> ", end="", flush=True)
        reply = call_deepseek(messages)
        if reply is None:
            # 出错时把最后一条用户消息移除，避免污染历史
            messages.pop()
            continue
        print(reply)
        # 把 AI 的回复也加入历史，多轮对话才能继续
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
