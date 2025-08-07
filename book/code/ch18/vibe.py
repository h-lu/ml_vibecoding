import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_deepseek import ChatDeepSeek

# 加载环境变量
load_dotenv()

# 1. 定义工具
search_tool = DuckDuckGoSearchRun()

# 2. 定义团队角色 (Agents)
# 使用 DeepSeek 模型初始化 LLM
llm = ChatDeepSeek(model="deepseek-chat")

# 新闻搜集员
researcher = Agent(
  role='精通网络搜索的专家',
  goal='从网络上找到关于AI领域的最新、最重大的新闻',
  backstory="""你是一名资深的新闻研究员，擅长使用高级搜索指令，
  快速地从海量信息中筛选出最相关、最权威的新闻来源。""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  llm=llm
)

# 资深分析师
analyst = Agent(
  role='经验丰富的技术市场分析师',
  goal='分析搜集到的新闻，识别出关键的技术趋势和对行业的商业影响',
  backstory="""你是一位在顶级咨询公司工作多年的市场分析师，
  对技术趋势有敏锐的嗅觉，能够从看似不相关的事件中，洞察出深刻的商业模式变革。""",
  verbose=True,
  allow_delegation=False,
  llm=llm
)

# 报告撰写人
writer = Agent(
  role='擅长将复杂技术概念转化为清晰易懂报告的科技作家',
  goal='根据分析师的洞察，撰写一篇结构清晰、语言流畅的综合性分析报告',
  backstory="""你是一位知名的科技专栏作家，你的文章以深入浅出、逻辑严密而著称，
  深受广大投资人和企业高管的喜爱。""",
  verbose=True,
  allow_delegation=True,
  llm=llm
)

# 3. 定义任务 (Tasks)
research_task = Task(
  description='查找并整理过去24小时内关于AI领域的5条最重要的新闻。',
  expected_output='一个包含5条新闻标题和链接的列表。',
  agent=researcher
)

analysis_task = Task(
  description='全面分析提供的新闻内容，总结出至少3个主要的技术趋势，并阐述它们各自的商业价值。',
  expected_output='一份详细的分析报告，包含清晰的趋势判断和商业价值分析。',
  agent=analyst,
  context=[research_task]
)

writing_task = Task(
  description='基于分析师的报告，撰写一篇面向非技术背景投资人的、500字左右的市场分析报告。',
  expected_output='一篇格式规范、语言流畅、观点鲜明的市场分析报告。',
  agent=writer,
  context=[analysis_task]
)

# 4. 组建团队与流程
market_analysis_crew = Crew(
  agents=[researcher, analyst, writer],
  tasks=[research_task, analysis_task, writing_task],
  process=Process.sequential,
  verbose=2
)

# 5. 启动任务
inputs = {}
result = market_analysis_crew.kickoff(inputs=inputs)
print("######################")
print("市场分析报告最终版:")
print(result)