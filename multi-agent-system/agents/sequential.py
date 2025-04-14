from google.adk.agents import SequentialAgent, LlmAgent

validator = LlmAgent(name="Validator", instruction="Check if input is valid.", output_key="status")
processor = LlmAgent(name="Processor", instruction="Process if status is valid.", output_key="processed")
reporter = LlmAgent(name="Reporter", instruction="Summarize from state['processed'].")

sequential_agent = SequentialAgent(
    name="SequentialWorkflow",
    sub_agents=[validator, processor, reporter]
)
