"""Triage agent — incident classification and IOC extraction."""

from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class TriageAgent(BaseAgent):
    """Triage incidents, classify severity, extract IOCs."""

    def __init__(self):
        super().__init__("Triage", "Incident Classifier", "venice")
        self.severity_levels = ["critical", "high", "medium", "low", "info"]
        self.ioc_types = ["ip", "domain", "hash", "filepath", "registry", "user", "process"]

    def process(self, incident_description: str) -> Dict[str, Any]:
        """Classify incident and extract IOCs."""
        self.add_message("user", incident_description)

        # Stub implementation — Phase 2 will use model reasoning
        iocs = self._extract_iocs(incident_description)
        severity = self._assess_severity(incident_description)
        category = self._classify_category(incident_description)

        result = {
            "triage": {
                "description": incident_description[:100],
                "severity": severity,
                "category": category,
                "ioc_count": len(iocs),
                "iocs": iocs,
                "recommended_actions": self._get_actions(severity, category),
            }
        }

        self.add_message("assistant", json.dumps(result))
        self.set_context("severity", severity)
        self.set_context("iocs", iocs)
        self.set_context("category", category)

        return result

    def _extract_iocs(self, text: str) -> List[Dict[str, str]]:
        """Extract IOCs from text."""
        import re
        iocs = []
        ip_pattern = r"\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\b"
        for match in re.finditer(ip_pattern, text):
            iocs.append({"type": "ip", "value": match.group()})
        return iocs[:5]  # Limit to first 5

    def _assess_severity(self, text: str) -> str:
        """Rough severity assessment."""
        keywords = {"critical": ["breach", "ransomware", "exfil"], "high": ["malware", "exploit"], "medium": ["suspicious"]}
        for sev, kws in keywords.items():
            if any(kw in text.lower() for kw in kws):
                return sev
        return "medium"

    def _classify_category(self, text: str) -> str:
        """Classify incident type."""
        if "malware" in text.lower():
            return "malware"
        if "ransomware" in text.lower():
            return "ransomware"
        if "breach" in text.lower():
            return "data_breach"
        return "suspicious_activity"

    def _get_actions(self, severity: str, category: str) -> List[str]:
        """Recommend immediate actions."""
        if severity == "critical":
            return ["Isolate affected systems", "Activate IR team", "Preserve evidence", "Notify leadership"]
        return ["Investigate", "Monitor", "Document"]