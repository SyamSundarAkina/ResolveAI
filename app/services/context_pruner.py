def prune_input_context(request: str, max_tokens: int = 300) -> str:
    """
    Simulated context pruning — trims overly long inputs.
    Replace with real MCP logic later if needed.
    """
    words = request.split()
    if len(words) > max_tokens:
        return " ".join(words[:max_tokens]) + " ..."
    return request
