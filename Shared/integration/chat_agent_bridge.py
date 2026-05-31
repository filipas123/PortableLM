"""Chat server <-> Agent router bridge for real incident response workflows."""
import json
from typing import Dict, Any
from agents.router import RouterAgent
from agents.triage import TriageAgent
from agents.detection_engineer import DetectionEngineerAgent
from agents.remediation import RemediationAgent
from agents.threat_intel import ThreatIntelAgent
from agents.ir_coordinator import IRCoordinatorAgent

class ChatAgentBridge:
    """Production bridge connecting chat server to real incident response agents."""
    
    def __init__(self):
        self.router = RouterAgent()
        self.agents = {
            "triage": TriageAgent(),
            "detection_engineer": DetectionEngineerAgent(),
            "remediation": RemediationAgent(),
            "threat_intel": ThreatIntelAgent(),
            "ir_coordinator": IRCoordinatorAgent(),
        }
    
    def process_query(self, user_input: str) -> Dict[str, Any]:
        """Route user query to appropriate specialized agent."""
        route = self.router.process(user_input)
        target_agent = route["target_agent"]
        agent = self.agents.get(target_agent)
        if agent:
            return agent.process(user_input)
        return {"error": f"Agent {target_agent} not found."}
