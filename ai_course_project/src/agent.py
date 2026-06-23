import re
from tools import get_current_week, calculate_gpa
from rag import rag_answer

# 全局对话记忆，保存最近对话
conversation_history = []


def agent_chat(user_input):
    """智能代理：根据用户输入路由到不同功能"""
    
    # 意图1：查询教学周
    week_keywords = ["第几周", "校历", "教学周", "这周", "本周", "星期", "周几", "几周", "周数"]
    if any(keyword in user_input for keyword in week_keywords):
        return get_current_week()
    
    # 意图2：计算绩点
    if "绩点" in user_input or "gpa" in user_input.lower():
        score_list = re.findall(r"\d+", user_input)
        if score_list:
            return calculate_gpa(",".join(score_list))
        else:
            return "请提供各科分数，格式参考：85,90,78"
    
    # 意图3：校园问题走RAG问答
    return rag_answer(user_input)


def chat_with_memory(user_input):
    """带记忆的对话"""
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})
    
    # 仅保留最近5轮对话上下文
    recent_context = conversation_history[-5:]
    
    # 获取回复
    reply = agent_chat(user_input)
    
    conversation_history.append({"role": "assistant", "content": reply})
    return reply


# 测试
if __name__ == "__main__":
    print("=" * 50)
    print("校园智能助手测试")
    print("=" * 50)
    
    # 测试用例
    test_queries = [
        "现在是第几教学周",
        "绩点怎么算，我考了85,90,78",
        "如何请病假",
        "奖学金需要多少绩点"
    ]
    
    for query in test_queries:
        print(f"\n用户：{query}")
        print(f"助手：{chat_with_memory(query)}")
        print("-" * 40)