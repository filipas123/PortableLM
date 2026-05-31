"""Remediation agent — generates automated fix plans."""

from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class RemediationAgent(BaseAgent):
    """Generate step-by-step remediation plans with automation."""

    def __init__(self):
        super().__init__("Remediation", "Automation Planner", "venice")

    def process(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        """Generate remediation plan."""
        self.add_message("user", f"Remediate: {json.dumps(incident)}")

        severity = incident.get("severity", "medium")
        category = incident.get("category", "unknown")

        immediate_actions = self._get_immediate_actions(severity)
        automation_steps = self._get_automation_runbook(category)
        validation_steps = self._get_validation_checks(category)

        result = {
            "remediation": {
                "severity": severity,
                "immediate_actions": immediate_actions,
                "automation_runbook": automation_steps,
                "validation_checks": validation_steps,
                "estimated_time_to_remediate": "4-8 hours",
            }
        }

        self.add_message("assistant", json.dumps(result))
        self.set_context("remediation_plan", result)

        return result

    def _get_immediate_actions(self, severity: str) -> List[str]:
        if severity == "critical":
            return ["Isolate affected host", "Kill malicious processes", "Block IPs", "Revoke compromised credentials"]
        return ["Quarantine file", "Stop service", "Monitor closely"]

    def _get_automation_runbook(self, category: str) -> List[Dict[str, str]]:
        return [
            {"step": 1, "action": "Block IPs in firewall", "tool": "firewall_api"},
            {"step": 2, "action": "Kill process", "tool": "edr_agent"},
            {"step": 3, "action": "Delete file", "tool": "file_removal"},
        ]

    def _get_validation_checks(self, category: str) -> List[str]:
        return [
            "Verify process termination",
            "Confirm file removal",
            "Check for persistence mechanisms",
            "Validate SIEM detection firing",
        ]