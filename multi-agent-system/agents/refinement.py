from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator

refiner = LlmAgent(
    name="Refiner",
    instruction="Improve code in state['code'] based on state['reqs'].",
    output_key="code"
)

checker = LlmAgent(
    name="Checker",
    instruction="Check if state['code'] meets state['reqs']. Output 'pass' or 'fail'.",
    output_key="status"
)

class StopCheck(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        if ctx.session.state.get("status") == "pass":
            yield Event(author=self.name, actions=EventActions(escalate=True))

refinement_loop = LoopAgent(
    name="RefinementLoop",
    max_iterations=5,
    sub_agents=[refiner, checker, StopCheck(name="Escalator")]
)
