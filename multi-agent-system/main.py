from fastapi import FastAPI, Request
from google.adk.runtime import AgentExecutor
from agents.coordinator import coordinator_agent
from agents.sequential import sequential_agent
from agents.parallel import parallel_workflow
from agents.refinement import refinement_loop
from agents.human_loop import approval_workflow
import os
import sys
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Add PYTHONPATH to sys.path if set
pythonpath = os.getenv("PYTHONPATH")
if pythonpath:
    sys.path.append(os.path.abspath(pythonpath))


app = FastAPI()

executors = {
    "coordinator": AgentExecutor(agent=coordinator_agent),
    "sequential": AgentExecutor(agent=sequential_agent),
    "parallel": AgentExecutor(agent=parallel_workflow),
    "refinement": AgentExecutor(agent=refinement_loop),
    "approval": AgentExecutor(agent=approval_workflow),
}

@app.post("/run/{agent_type}")
async def run_agent(agent_type: str, request: Request):
    data = await request.json()
    message = data.get("message", "")
    executor = executors.get(agent_type)

    if not executor:
        return {"error": f"Unknown agent type: {agent_type}"}

    session = await executor.start()
    response = await session.send(message)
    return {"response": response}
