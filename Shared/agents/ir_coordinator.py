"""IR Coordinator agent — orchestrates full incident response."""

from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class IRCoordinatorAgent(BaseAgent):
    """Orchestrate multi-step incident response workflow."""

    def __init__(self):
        super().__init__("IRCoordinator", "Response Orchestrator", "venice")
        self.ir_phases = ["Detection", "Analysis", "Containment", "Eradication", "Recovery", "Post-Incident"]

    def process(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate full IR response."""
        self.add_message("user", f"Coordinate IR response: {json.dumps(incident)}")

        ir_plan = self._build_ir_plan(incident)
        timeline = self._build_incident_timeline(incident)
        status = self._init_response_status()

        result = {
            "ir_coordinator": {
                "ir_phases": ir_plan,
                "timeline": timeline,
                "status": status,
                "escalation_path": ["SOC Analyst", "IR Manager", "CISO", "Executive"],
            }
        }

        self.add_message("assistant", json.dumps(result))
        self.set_context("ir_plan", ir_plan)
        self.set_context("status", status)

        return result

    def _build_ir_plan(self, incident: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"phase": "Detection", "status": "complete", "owner": "SOC"},
            {"phase": "Analysis", "status": "in_progress", "owner": "IR Team"},
            {"phase": "Containment", "status": "pending", "owner": "IR Team"},
            {"phase": "Eradication", "status": "pending", "owner": "System Admin"},
            {"phase": "Recovery", "status": "pending", "owner": "System Admin"},
            {"phase": "Post-Incident", "status": "pending", "owner": "Management"},
        ]

    def _build_incident_timeline(self, incident: Dict[str, Any]) -> List[Dict[str, str]]:
        return [
            {"time": "2024-01-01T10:00:00Z", "event": "Initial detection by SIEM"},
            {"time": "2024-01-01T10:15:00Z", "event": "Alert escalated to SOC"},
            {"time": "2024-01-01T10:30:00Z", "event": "IR team engaged"},
        ]

    def _init_response_status(self) -> Dict[str, str]:
        return {
            "incident_status": "active",
            "containment_status": "not_started",
            "affected_systems": "5",
            "data_exfiltrated": "unknown",
        }