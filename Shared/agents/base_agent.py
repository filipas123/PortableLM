"""Base agent class with shared context and message history."""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime

class BaseAgent:
    """Base agent with shared context, message history, and provider abstraction."""

    def __init__(self, name: str, role: str, provider_id: str = "venice"):
        self.name = name
        self.role = role
        self.provider_id = provider_id
        self.messages: List[Dict[str, str]] = []
        self.context: Dict[str, Any] = {}
        self.created_at = datetime.utcnow().isoformat() + "Z"

    def add_message(self, role: str, content: str):
        """Add message to history."""
        self.messages.append({"role": role, "content": content, "timestamp": datetime.utcnow().isoformat() + "Z"})

    def set_context(self, key: str, value: Any):
        """Set shared context variable."""
        self.context[key] = value

    def get_context(self, key: str) -> Optional[Any]:
        """Get shared context variable."""
        return self.context.get(key)

    def process(self, user_input: str) -> str:
        """Process user input and return response. Override in subclasses."""
        raise NotImplementedError

    def serialize(self) -> Dict[str, Any]:
        """Serialize agent state."""
        return {
            "name": self.name,
            "role": self.role,
            "provider": self.provider_id,
            "created_at": self.created_at,
            "message_count": len(self.messages),
            "context_keys": list(self.context.keys()),
        }