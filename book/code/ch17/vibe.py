"""
本脚本演示了如何使用 LangGraph 和 DeepSeek 模型构建一个有状态的差旅审批流程。

核心功能：
1.  **状态管理**: 使用 TypedDict 定义图的共享状态，跟踪申请信息和审批决定。
2.  **条件路由**: 根据报销金额（<500元）决定是自动批准还是需要经理审批。
3.  **工具使用**: 定义并调用一个工具来查询员工的历史报销记录。
4.  **大模型集成**: 利用 DeepSeek 的聊天模型，模拟经理根据综合信息（申请详情、历史记录）进行决策。
5.  **端到端流程**: 完整实现了从申请提交到最终决策的图流程，并提供了两个不同场景的调用示例。

运行前，请确保已安装所需库:
`pip install langgraph langchain_deepseek python-dotenv`

并设置环境变量 `DEEPSEEK_API_KEY`，或在项目根目录创建 `.env` 文件并写入：
`DEEPSEEK_API_KEY="your_deepseek_api_key"`
"""

import os
from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# --- 1. 定义图的状态 ---
class GraphState(TypedDict):
    """
    定义图的状态

    Attributes:
        employee_name: 申请人姓名
        amount: 申请金额
        reason: 事由
        history_check_result: 历史记录检查结果
        decision: 最终决定 ("自动批准", "批准", "拒绝")
        messages: 交流消息列表
    """
    employee_name: str
    amount: int
    reason: str
    history_check_result: str
    decision: str
    messages: Annotated[List[BaseMessage], operator.add]


# --- 2. 定义工具 ---
def query_employee_history(employee_name: str) -> str:
    """
    一个模拟的工具，用于查询员工的历史报销记录。
    在真实场景中，这里会连接到公司的数据库或API。
    """
    print(f"--- 工具调用：正在查询 {employee_name} 的历史记录... ---")
    # 模拟返回结果
    if "王" in employee_name:
        return f"员工 {employee_name} 的历史报销记录良好，无异常。"
    else:
        return f"员工 {employee_name} 在过去一年内有两次大额报销记录，需要注意。"

# --- 3. 定义图的节点 ---

def direct_approval_node(state: GraphState) -> dict:
    """直接批准节点：更新状态为自动批准"""
    print("--- 节点：进入直接批准流程 ---")
    return {"decision": "自动批准"}

def manager_approval_node(state: GraphState) -> dict:
    """经理审批节点：调用工具和LLM进行决策"""
    print("--- 节点：进入经理审批流程 ---")
    
    # 1. 调用工具查询历史记录
    history = query_employee_history(state["employee_name"])
    
    # 2. 准备与 LLM 交互
    llm = ChatDeepSeek(model="deepseek-chat")
    
    # 3. 构建提示
    prompt = f"""
    你是一位严谨负责的部门经理，你需要对下属的差旅报销申请做出审批。
    请根据以下信息，给出“批准”或“拒绝”的最终决定，不要包含任何其他解释。

    申请信息：
    - 申请人: {state['employee_name']}
    - 报销金额: {state['amount']}元
    - 事由: {state['reason']}

    背景调查（人力资源系统）:
    - {history}

    你的决定是（请只回答“批准”或“拒绝”）:
    """
    
    messages = [HumanMessage(content=prompt)]
    
    # 4. 调用 LLM
    print("--- LLM调用：正在请求经理决策... ---")
    response = llm.invoke(messages)
    decision = response.content
    
    print(f"--- LLM决策结果：{decision} ---")

    return {
        "history_check_result": history,
        "decision": decision
    }

# --- 4. 定义条件路由 ---

def should_go_to_manager(state: GraphState) -> str:
    """根据金额判断路由方向"""
    print("--- 入口路由：检查报销金额 ---")
    if state["amount"] < 500:
        print(f"--- 金额 {state['amount']} < 500，走向“直接批准” ---")
        return "direct_approval"
    else:
        print(f"--- 金额 {state['amount']} >= 500，走向“经理审批” ---")
        return "manager_approval"

# --- 5. 构建图 ---
print("构建审批流程图...")
workflow = StateGraph(GraphState)

# 添加节点
workflow.add_node("direct_approval", direct_approval_node)
workflow.add_node("manager_approval", manager_approval_node)

# 设置入口点和条件路由
workflow.set_conditional_entry_point(
    should_go_to_manager,
    {
        "direct_approval": "direct_approval",
        "manager_approval": "manager_approval",
    },
)

# 添加从节点到终点的边
workflow.add_edge("direct_approval", END)
workflow.add_edge("manager_approval", END)

# 编译图
app = workflow.compile()
print("审批流程图构建完成！\n")

# --- 6. 提供调用示例 ---

# 示例1: 小额报销，应自动批准
print("====== 案例1: 小额报销 ======")
small_expense_input = {
    "employee_name": "张三",
    "amount": 300,
    "reason": "市内交通费",
    "messages": []
}
final_state_small = app.invoke(small_expense_input)
print("\n--- 最终审批结果 [小额] ---")
print(final_state_small)
print("============================\n")


# 示例2: 大额报销，需要经理审批
print("====== 案例2: 大额报销 ======")
large_expense_input = {
    "employee_name": "李四",
    "amount": 5000,
    "reason": "交通费",
    "messages": []
}
final_state_large = app.invoke(large_expense_input)
print("\n--- 最终审批结果 [大额] ---")
print(final_state_large)
print("============================")

