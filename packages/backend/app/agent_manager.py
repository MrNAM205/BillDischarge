import importlib
from typing import Dict, Any

from modules.config_manager import config
from agents.base_agent import BaseAgent

class AgentManager:
    """
    Manages the loading and orchestration of VeroBrix agents.
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self._load_agents()

    def _load_agents(self):
        """
        Dynamically loads agents based on the configuration file.
        """
        agent_configs = config.get_section('agents')
        for agent_name, agent_config in agent_configs.items():
            if agent_config.get('enabled', False):
                try:
                    module_path = f"agents.{agent_name.upper()}.{agent_name.lower()}_agent"
                    agent_module = importlib.import_module(module_path)
                    
                    # Convention: Class name is PascalCase version of agent name (e.g., 'jarvis' -> 'JarvisAgent')
                    class_name = f"{agent_name.capitalize()}Agent"
                    agent_class = getattr(agent_module, class_name)
                    
                    self.agents[agent_name] = agent_class(agent_config)
                    print(f"Successfully loaded agent: {agent_name}") # Placeholder for proper logging
                except (ImportError, AttributeError) as e:
                    print(f"Error loading agent '{agent_name}': {e}") # Placeholder for proper logging

    def get_agent(self, agent_name: str) -> BaseAgent:
        """
        Retrieves a loaded agent by name.
        """
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' is not loaded or does not exist.")
        return agent
