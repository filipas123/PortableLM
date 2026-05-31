"""Chain-of-custody evidence tracking."""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class EvidenceManager:
    """Track evidence chain-of-custody with hashing and versioning."""

    def __init__(self, evidence_root: Path):
        self.evidence_root = evidence_root
        self.evidence_root.mkdir(parents=True, exist_ok=True)
        self.manifest: Dict[str, Any] = {}

    def add_evidence(self, evidence_id: str, file_path: Path, collected_by: str, description: str) -> Dict[str, str]:
        """Add evidence file to chain-of-custody."""
        file_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
        entry = {
            "evidence_id": evidence_id,
            "file_path": str(file_path),
            "file_hash": file_hash,
            "collected_by": collected_by,
            "collected_at": datetime.utcnow().isoformat() + "Z",
            "description": description,
            "status": "collected",
        }
        self.manifest[evidence_id] = entry
        return entry

    def save_manifest(self):
        """Save manifest to disk."""
        manifest_path = self.evidence_root / "manifest.json"
        manifest_path.write_text(json.dumps(self.manifest, indent=2))

    def verify_integrity(self, evidence_id: str, file_path: Path) -> bool:
        """Verify evidence hash hasn't changed."""
        if evidence_id not in self.manifest:
            return False
        original_hash = self.manifest[evidence_id]["file_hash"]
        current_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
        return original_hash == current_hash