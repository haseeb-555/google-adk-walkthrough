from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.tools import FunctionTool
from utils.external_approval import external_approval_tool

prepare = LlmAgent(
    name="Prepare",
    instruction="Store approval_amount and approval_reason in state."
)

approval = LlmAgent(
    name="Approval",
    instruction="Use tool to get human approval for state['approval_amount'], state['approval_reason'].",
    tools=[FunctionTool(func=external_approval_tool)],
    output_key="human_decision"
)

decision = LlmAgent(
    name="Decision",
    instruction="Read state['human_decision'] and proceed."
)

approval_workflow = SequentialAgent(
    name="HumanLoopWorkflow",
    sub_agents=[prepare, approval, decision]
)
