"""Immutable audit logger."""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    """Write immutable audit trail with SHA256 chain."""

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.last_hash = None

    def log(self, action: str, user: str, resource: str, details: Dict[str, Any]) -> str:
        """Log action with hash chain."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "user": user,
            "resource": resource,
            "details": details,
            "previous_hash": self.last_hash,
        }
        entry_json = json.dumps(entry)
        entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        entry["hash"] = entry_hash
        self.log_path.write_text(json.dumps(entry) + "\n", encoding="utf-8", mode="a")
        self.last_hash = entry_hash
        return entry_hash