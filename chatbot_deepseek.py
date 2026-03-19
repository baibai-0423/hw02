import os  # 用于读取环境变量
import requests  # 用于发送 HTTP 请求调用 API

# -------------------------- 配置区（从环境变量读取，避免硬编码） --------------------------
# 从系统环境变量中获取 DeepSeek API Key，避免将敏感信息写入代码
API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    raise ValueError("❌ 未找到环境变量 DEEPSEEK_API_KEY，请先配置 API Key！")

# DeepSeek API 官方接口地址（固定不变）
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 请求头：指定数据格式和授权信息
HEADERS = {
    "Content-Type": "application/json",  # 数据格式为 JSON
    "Authorization": f"Bearer {API_KEY}"   # 授权方式：Bearer + API Key
}

# -------------------------- 核心对话函数 --------------------------
def chat_with_deepseek(user_input: str, model: str = "deepseek-chat", temperature: float = 0.7) -> str:
    """
    调用 DeepSeek API 进行对话
    
    参数:
        user_input: str - 用户输入的问题/内容
        model: str - 使用的模型名称，可选 deepseek-chat / deepseek-code
        temperature: float - 温度值，控制输出随机性（0~2，越小越确定性，越大越随机）
    
    返回:
        str - 模型返回的回答内容，或错误信息
    """
    # 构造 API 请求的 JSON 数据
    payload = {
        "model": model,  # 指定使用的模型
        "messages": [     # 对话上下文，这里是单轮对话
            {"role": "user", "content": user_input}
        ],
        "temperature": temperature,  # 控制输出多样性
        "max_tokens": 2048,          # 单次请求最大 Token 数，限制回答长度
        "stream": False              # 关闭流式输出，一次性获取完整回答
    }

    try:
        # 发送 POST 请求到 DeepSeek API
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        # 检查请求是否成功（状态码 200 表示成功）
        response.raise_for_status()
        # 解析 JSON 响应
        result = response.json()
        # 提取模型生成的回答内容
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        # 捕获网络请求相关错误（如超时、连接失败）
        return f"❌ 网络请求失败：{str(e)}"
    except KeyError:
        # 捕获 JSON 解析错误（如 API 返回格式异常）
        return "❌ API 返回格式异常，无法解析回答"
    except Exception as e:
        # 捕获其他未知错误
        return f"❌ 未知错误：{str(e)}"

# -------------------------- 交互式对话入口 --------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 DeepSeek Chatbot 已启动（输入 'quit' 或 'exit' 退出对话）")
    print("=" * 50)
    
    while True:
        # 获取用户输入
        user_input = input("\n你：")
        # 退出对话判断
        if user_input.strip().lower() in ["quit", "exit", "q"]:
            print("\n👋 对话结束，感谢使用！")
            break
        # 空输入处理
        if not user_input.strip():
            print("⚠️  请输入有效内容，不要发送空消息~")
            continue
        # 调用函数获取回答
        print("💬 Chatbot 正在思考...")
        reply = chat_with_deepseek(user_input)
        # 打印回答
        print(f"\nChatbot：{reply}")