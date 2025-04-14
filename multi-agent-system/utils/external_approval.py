async def external_approval_tool(amount: float, reason: str) -> str:
    print(f"Approval needed for ₹{amount} due to: {reason}")
    # Simulate human approval
    return "approved" if amount < 1000 else "rejected"
