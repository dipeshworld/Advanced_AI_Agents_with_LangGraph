# 1. Imports & Setup
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import operator
import re
import ast


# 2. Define State
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]


# 3. Math Functions (TOOLS)
def plus(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b


# 4. Normalize Input
def normalize_expression(text: str):
    text = text.lower()

    replacements = {
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "times": "*",
        "multiply": "*",
        "multiplied by": "*",
        "divide": "/",
        "divided by": "/"
    }

    for word, symbol in replacements.items():
        text = text.replace(word, symbol)

    return text


# 5. Extract Expression
def extract_expression(text: str):
    expr = re.findall(r"[0-9\.\+\-\*/\(\)\s]+", text)
    return "".join(expr).strip()


# 6. Safe AST Evaluation
def evaluate_ast(node):
    if isinstance(node, ast.Expression):
        return evaluate_ast(node.body)

    elif isinstance(node, ast.BinOp):
        left = evaluate_ast(node.left)
        right = evaluate_ast(node.right)

        if isinstance(node.op, ast.Add):
            return plus(left, right)
        elif isinstance(node.op, ast.Sub):
            return subtract(left, right)
        elif isinstance(node.op, ast.Mult):
            return multiply(left, right)
        elif isinstance(node.op, ast.Div):
            return divide(left, right)

    elif isinstance(node, ast.Num):
        return node.n

    elif isinstance(node, ast.Constant):
        return node.value

    else:
        raise ValueError("Unsupported expression")


# 7. Solve Math
def solve_math_expression(text: str):
    try:
        normalized = normalize_expression(text)
        expr = extract_expression(normalized)

        if not expr:
            return None

        parsed = ast.parse(expr, mode='eval')
        result = evaluate_ast(parsed)

        return result

    except Exception:
        return None


# 8. Nodes

# LLM Node
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def chatbot_node(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# Math Node
def math_node(state: AgentState):
    user_input = state["messages"][-1].content

    result = solve_math_expression(user_input)

    if result is None:
        return {"messages": [AIMessage(content="Could not parse math query.")]}

    return {"messages": [AIMessage(content=f"Result: {result}")]}


# 9. Router
def router(state: AgentState):
    user_input = state["messages"][-1].content

    result = solve_math_expression(user_input)

    if result is not None:
        return "math"

    return "chatbot"


# 10. Build LangGraph
graph = StateGraph(AgentState)

graph.add_node("chatbot", chatbot_node)
graph.add_node("math", math_node)

graph.set_entry_point("chatbot")

graph.add_conditional_edges(
    "chatbot",
    router,
    {
        "math": "math",
        "chatbot": END
    }
)

graph.add_edge("math", END)

app = graph.compile()


# 11. Run Queries
def run_query(query: str):
    result = app.invoke({
        "messages": [HumanMessage(content=query)]
    })
    return result["messages"][-1].content


# 12. Run Examples
if __name__ == "__main__":
    print("---- General ----")
    print(run_query("What is data engineering?"))

    print("\n---- Basic Math ----")
    print(run_query("4+14"))
    print(run_query("10 divided by 2"))

    print("\n---- Multi-step Math ----")
    print(run_query("4 + 5 * 2"))
    print(run_query("10 + (6/2)"))
    print(run_query("100 / (5 + 5)"))

    print("\n---- Natural Language ----")
    print(run_query("What is 4 plus 5 times 2?"))

    print("\n---- Edge Case ----")
    print(run_query("10 / 0"))