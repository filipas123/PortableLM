"""Threat Intelligence agent — MITRE mapping, enrichment, correlation."""

from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class ThreatIntelAgent(BaseAgent):
    """Map TTPs to MITRE ATT&CK, enrich IOCs, correlate with threat actors."""

    def __init__(self):
        super().__init__("ThreatIntel", "Intelligence Analyst", "venice")

    def process(self, iocs: List[Dict[str, str]], incident_description: str) -> Dict[str, Any]:
        """Analyze IOCs and generate threat intelligence."""
        self.add_message("user", f"Analyze IOCs: {json.dumps(iocs)}")

        mitre_techniques = self._map_to_mitre(incident_description)
        enriched_iocs = self._enrich_iocs(iocs)
        correlated_actors = self._correlate_threat_actors(mitre_techniques)

        result = {
            "threat_intel": {
                "mitre_techniques": mitre_techniques,
                "enriched_iocs": enriched_iocs,
                "threat_actors": correlated_actors,
                "risk_score": 7.5,
            }
        }

        self.add_message("assistant", json.dumps(result))
        self.set_context("mitre_techniques", mitre_techniques)
        self.set_context("threat_actors", correlated_actors)

        return result

    def _map_to_mitre(self, description: str) -> List[Dict[str, str]]:
        return [
            {"technique_id": "T1566.001", "technique_name": "Phishing: Spearphishing Attachment", "tactic": "Initial Access"},
            {"technique_id": "T1059.001", "technique_name": "Command and Scripting Interpreter: PowerShell", "tactic": "Execution"},
        ]

    def _enrich_iocs(self, iocs: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        enriched = []
        for ioc in iocs:
            enriched.append({
                "ioc": ioc,
                "reputation": "malicious",
                "first_seen": "2024-01-01",
                "threat_intel_sources": ["AlienVault OTX", "Shodan"],
            })
        return enriched

    def _correlate_threat_actors(self, techniques: List[Dict[str, str]]) -> List[Dict[str, str]]:
        return [
            {"actor_id": "APT29", "name": "Cozy Bear", "confidence": "medium"},
            {"actor_id": "FIN7", "name": "Fin7", "confidence": "low"},
        ]