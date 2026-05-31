"""Router agent — routes queries to specialized agents."""

from .base_agent import BaseAgent
from typing import Dict, Any, Optional

class RouterAgent(BaseAgent):
    """Routes queries to appropriate specialized agents based on query content."""

    def __init__(self):
        super().__init__("Router", "Query Router", "venice")
        self.specialization_map = {
            "incident": "triage",
            "alert": "triage",
            "malware": "triage",
            "detection": "detection_engineer",
            "sigma": "detection_engineer",
            "remediation": "remediation",
            "fix": "remediation",
            "threat": "threat_intel",
            "mitre": "threat_intel",
            "response": "ir_coordinator",
            "containment": "ir_coordinator",
        }

    def process(self, user_input: str) -> Dict[str, Any]:
        """Analyze input and route to specialized agent."""
        self.add_message("user", user_input)

        query_lower = user_input.lower()
        target_agent = None

        # Keyword matching for agent selection
        for keyword, agent in self.specialization_map.items():
            if keyword in query_lower:
                target_agent = agent
                break

        if not target_agent:
            target_agent = "triage"  # Default to triage

        response = {
            "router": "analyzing",
            "query": user_input,
            "target_agent": target_agent,
            "confidence": 0.85 if target_agent != "triage" else 0.6,
            "reason": f"Routed to {target_agent} based on query keywords.",
        }

        self.add_message("assistant", json.dumps(response))
        self.set_context("last_route", target_agent)

        return response

import json