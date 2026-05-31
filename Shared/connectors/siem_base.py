"""Abstract SIEM connector base class."""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

class SIEMConnector(ABC):
    """Base class for SIEM connectors."""

    def __init__(self, name: str, api_url: str, api_key: str):
        self.name = name
        self.api_url = api_url
        self.api_key = api_key
        self.is_connected = False

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to SIEM."""
        pass

    @abstractmethod
    def search(self, query: str, time_range: str = "24h") -> List[Dict[str, Any]]:
        """Execute search query."""
        pass

    @abstractmethod
    def create_alert(self, title: str, description: str, severity: str) -> str:
        """Create alert in SIEM."""
        pass

    @abstractmethod
    def create_saved_search(self, name: str, query: str) -> str:
        """Create saved search."""
        pass

    def disconnect(self):
        """Disconnect from SIEM."""
        self.is_connected = False