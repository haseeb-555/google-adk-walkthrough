from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()

# Now you can access the API key
api_key = os.getenv("GOOGLE_API_KEY")

# --- Constants ---
APP_NAME = "code_pipeline_app"
USER_ID = "dev_user_01"
SESSION_ID = "pipeline_session_01"
GEMINI_MODEL = "gemini-2.0-flash-exp"

os.environ["GOOGLE_API_KEY"] = api_key


# --- 1. Define Sub-Agents for Each Pipeline Stage ---

# Code Writer Agent
code_writer_agent = LlmAgent(
    name="CodeWriterAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Code Writer AI.
    Based on the user's request, write the initial Python code.
    Output *only* the raw code block.
    """,
    description="Writes initial code based on a specification.",
    output_key="generated_code"
)

# Code Reviewer Agent
code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Code Reviewer AI.
    Review the Python code provided in the session state under the key 'generated_code'.
    Provide constructive feedback on potential errors, style issues, or improvements.
    Focus on clarity and correctness.
    Output only the review comments.
    """,
    description="Reviews code and provides feedback.",
    output_key="review_comments"
)

# Code Refactorer Agent
code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Code Refactorer AI.
    Take the original Python code provided in the session state key 'generated_code'
    and the review comments found in the session state key 'review_comments'.
    Refactor the original code to address the feedback and improve its quality.
    Output *only* the final, refactored code block.
    """,
    description="Refactors code based on review comments.",
    output_key="refactored_code"
)

# --- 2. Create the SequentialAgent ---
code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent]
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=code_pipeline_agent, app_name=APP_NAME, session_service=session_service)

# Agent Interaction Function
def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    # Print Final Output
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("\n✅ Final Refactored Code:\n", final_response)

    # Print Intermediate State Values
    state = session.state
    print("\n🛠️ Intermediate Pipeline Outputs:")
    print("\n🔹 Generated Code:\n", state.get("generated_code"))
    print("\n🔹 Review Comments:\n", state.get("review_comments"))
    print("\n🔹 Refactored Code:\n", state.get("refactored_code"))

# --- Entry Point ---
if __name__ == "__main__":
    call_agent("perform code of bfs traversal in java")
