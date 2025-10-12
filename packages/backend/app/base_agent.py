from typing import Any, Dict, List

class BaseAgent:
    """Base class for all VeroBrix agents."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def analyze(self, input_data: Any, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main analysis method - must be implemented by all agents."""
        raise NotImplementedError("Each agent must implement its own analyze method.")

    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        raise NotImplementedError("Each agent must declare its capabilities.")
