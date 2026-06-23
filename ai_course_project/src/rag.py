import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_templates import RAG_PROMPT
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 加载环境变量密钥
load_dotenv()

# ========== 独立加载向量库 ==========
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

script_dir = os.path.dirname(os.path.abspath(__file__))
vector_db_path = os.path.join(script_dir, "../vector_db")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh",
    cache_folder="./model_cache"
)

vector_db = Chroma(
    persist_directory=vector_db_path,
    embedding_function=embeddings
)

# ========== 初始化客户端（使用环境变量） ==========
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # 从环境变量获取
    timeout=60
)

# ========== RAG 问答函数 ==========
def rag_answer(question):
    # 1. 向量库检索相关知识库
    docs = vector_db.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    # 2. 拼接提示词调用大模型
    prompt = RAG_PROMPT.format(context=context, question=question)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# 测试
if __name__ == "__main__":
    print(rag_answer("奖学金需要多少绩点"))