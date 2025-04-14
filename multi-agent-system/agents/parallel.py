from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent

api1 = LlmAgent(name="API1", instruction="Fetch API1 data.", output_key="api1")
api2 = LlmAgent(name="API2", instruction="Fetch API2 data.", output_key="api2")
synth = LlmAgent(name="Synth", instruction="Combine API1 and API2 from state.")

parallel_gather = ParallelAgent(name="Fetcher", sub_agents=[api1, api2])

parallel_workflow = SequentialAgent(
    name="ParallelWorkflow",
    sub_agents=[parallel_gather, synth]
)
