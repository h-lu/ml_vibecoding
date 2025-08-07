# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 设置 TOKENIZERS_PARALLELISM 环境变量以避免警告
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_deepseek import ChatDeepSeek

# 1. 文档加载
file_paths = [
    "data/policy_health_insurance.txt",
    "data/policy_vacation.txt",
    "data/policy_travel_reimbursement.txt"
]

# 加载所有文档
docs = []
for path in file_paths:
    loader = TextLoader(path, encoding='utf-8')
    docs.extend(loader.load())

# 2. 文本分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separators=["\n\n", "\n", "。", "！", "？", "，", "、", " "]
)
split_docs = text_splitter.split_documents(docs)

# 3. 嵌入与存储
# 使用本地嵌入模型 (需要先安装: pip install sentence-transformers)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 创建ChromaDB向量数据库 (需要先安装: pip install chromadb)
vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory="./chroma_db")

# 4. 创建RAG链
# 创建检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 定义提示模板 (中文模板)
prompt_template = """
你是一个公司政策问答助手，请根据以下上下文信息回答问题：
<上下文>
{context}
</上下文>

问题：{input}
请用中文简洁明了地回答，如果不知道答案就说"根据现有政策无法回答"。
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

# 初始化DeepSeek模型 (需要设置DEEPSEEK_API_KEY环境变量)
# 替代方案: 如果没有API key，可使用其他本地模型如Ollama
llm = ChatDeepSeek(model="deepseek-chat", temperature=0.1)

# 组合文档链
document_chain = create_stuff_documents_chain(llm, prompt)

# 创建检索链
rag_chain = create_retrieval_chain(retriever, document_chain)

# 5. 测试
question = "我工作5年了, 去年请了13天年假, 我今年的年假有多少天？"
response = rag_chain.invoke({"input": question})

# 打印结果
print("问题：", question)
print("答案：", response["answer"])
print("\n相关文档片段：")
for i, doc in enumerate(response["context"]):
    print(f"\n片段 {i+1}:")
    print(doc.page_content[:100] + "...")  # 只打印前100字符