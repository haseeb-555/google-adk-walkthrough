from google.adk.agents import LlmAgent

billing = LlmAgent(name="Billing", description="Handles billing inquiries.")
support = LlmAgent(name="Support", description="Handles tech issues.")

coordinator_agent = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="Route user requests to Billing or Support.",
    description="Routes queries to the right department.",
    sub_agents=[billing, support]
)
