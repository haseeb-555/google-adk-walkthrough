import os
from dotenv import load_dotenv

from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
from google.genai import types

# --- Load API Key ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY in .env file")
os.environ["GOOGLE_API_KEY"] = api_key

# --- Constants ---
APP_NAME = "parallel_research_app"
USER_ID = "research_user_01"
SESSION_ID = "parallel_research_session"
GEMINI_MODEL = "gemini-2.0-flash-exp"

# --- Define Researcher Sub-Agents ---

# 1. Renewable Energy
researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in energy.
    Research the latest advancements in 'renewable energy sources'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.
    """,
    description="Researches renewable energy sources.",
    tools=[google_search],
    output_key="renewable_energy_result"
)

# 2. Electric Vehicles
researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in transportation.
    Research the latest developments in 'electric vehicle technology'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.
    """,
    description="Researches electric vehicle technology.",
    tools=[google_search],
    output_key="ev_technology_result"
)

# 3. Carbon Capture
researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in climate solutions.
    Research the current state of 'carbon capture methods'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.
    """,
    description="Researches carbon capture methods.",
    tools=[google_search],
    output_key="carbon_capture_result"
)

# 4. Large Language Models (LLMs)
researcher_agent_4 = LlmAgent(
    name="LLMResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant focusing on language models.
    Research the latest innovations in large language models (LLMs), including architecture improvements and applications.
    Use the Google Search tool provided.
    Summarize your findings in 1-2 concise sentences.
    Output *only* the summary.
    """,
    description="Researches advancements in LLMs.",
    tools=[google_search],
    output_key="llm_result"
)

# 5. Quantum Computing
researcher_agent_5 = LlmAgent(
    name="QuantumComputingResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in quantum computing.
    Research recent progress in quantum algorithms, hardware, or real-world applications.
    Use the Google Search tool provided.
    Summarize your findings in 1-2 concise sentences.
    Output *only* the summary.
    """,
    description="Explores quantum computing progress.",
    tools=[google_search],
    output_key="quantum_computing_result"
)

# 6. Data Privacy / "Using data without seeing it"
researcher_agent_6 = LlmAgent(
    name="PrivacyDataResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant interested in data privacy.
    Research techniques that allow use of data without directly accessing it — such as federated learning, differential privacy, or synthetic data.
    Use the Google Search tool provided.
    Summarize your findings in 1-2 sentences.
    Output *only* the summary.
    """,
    description="Researches privacy-preserving data usage methods.",
    tools=[google_search],
    output_key="privacy_data_result"
)

# --- Orchestrate with ParallelAgent ---

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[
        researcher_agent_1,
        researcher_agent_2,
        researcher_agent_3,
        researcher_agent_4,
        researcher_agent_5,
        researcher_agent_6
    ]
)

# --- Session and Runner ---
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)
runner = Runner(agent=parallel_research_agent, app_name=APP_NAME, session_service=session_service)

# --- Interaction Function ---

def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:\n", final_response)

# --- Run Main ---
if __name__ == "__main__":
    call_agent("research latest trends")
