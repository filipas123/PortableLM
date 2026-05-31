"""Microsoft Sentinel connector."""

from .siem_base import SIEMConnector
from typing import Dict, Any, List

class SentinelConnector(SIEMConnector):
    """Microsoft Sentinel (Azure Monitor) connector."""

    def __init__(self, api_url: str, api_key: str, workspace_id: str):
        super().__init__("Sentinel", api_url, api_key)
        self.workspace_id = workspace_id

    def connect(self) -> bool:
        self.is_connected = True
        return True

    def search(self, query: str, time_range: str = "24h") -> List[Dict[str, Any]]:
        kql_query = f"{query} | where TimeGenerated > ago({time_range})"
        return [{"kql": kql_query, "workspace": self.workspace_id, "status": "would_execute"}]

    def create_alert(self, title: str, description: str, severity: str) -> str:
        alert_id = f"sentinel_incident_{id(title)}"
        return alert_id

    def create_saved_search(self, name: str, query: str) -> str:
        search_id = f"sentinel_rule_{id(name)}"
        return search_id