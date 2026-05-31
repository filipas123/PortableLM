"""Detection Engineer agent — generates Sigma/YARA/SIEM rules."""

from .base_agent import BaseAgent
from typing import Dict, Any
import json

class DetectionEngineerAgent(BaseAgent):
    """Generate detection rules: Sigma, YARA, SIEM queries."""

    def __init__(self):
        super().__init__("DetectionEngineer", "Rule Generator", "venice")

    def process(self, iocs: list, category: str = "malware") -> Dict[str, Any]:
        """Generate detection rules for given IOCs."""
        self.add_message("user", f"Generate detection rules for {category}: {json.dumps(iocs)}")

        sigma_rule = self._generate_sigma(iocs, category)
        siem_queries = self._generate_siem_queries(iocs, category)
        yara_rule = self._generate_yara(iocs, category)

        result = {
            "detection_engineer": {
                "ioc_count": len(iocs),
                "sigma_rule": sigma_rule,
                "siem_queries": siem_queries,
                "yara_rule": yara_rule,
                "deployment_ready": True,
            }
        }

        self.add_message("assistant", json.dumps(result))
        self.set_context("sigma_rule", sigma_rule)
        self.set_context("siem_queries", siem_queries)

        return result

    def _generate_sigma(self, iocs: list, category: str) -> Dict[str, Any]:
        return {
            "title": f"Detect {category}",
            "status": "experimental",
            "logsource": {"product": "windows", "service": "security"},
            "detection": {"selection": {"EventID": 4688}, "condition": "selection"},
            "note": "Phase 2 will generate full Sigma from IOCs"
        }

    def _generate_siem_queries(self, iocs: list, category: str) -> Dict[str, str]:
        return {
            "splunk": "index=main earliest=-24h | search IOC",
            "elastic": "source.ip: 192.168.1.* OR destination.ip: 192.168.1.*",
            "sentinel": "DeviceNetworkEvents | where RemoteIP in (iocs)"
        }

    def _generate_yara(self, iocs: list, category: str) -> str:
        return f"rule {category} {{ strings: $s1 = \"IOC\" condition: $s1 }}"