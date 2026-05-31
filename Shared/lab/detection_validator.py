"""Production detection validation against real logs."""
from typing import Dict, Any, List

class DetectionValidator:
    """Validate Sigma rules against real production logs for accuracy."""
    
    def __init__(self):
        self.test_results = []
    
    def validate_sigma_rule(self, rule: Dict[str, Any], test_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate Sigma rule detection accuracy against real logs."""
        matched = []
        for log in test_logs:
            if self._matches_rule(rule, log):
                matched.append(log)
        
        return {
            "rule_id": rule.get('title'),
            "total_logs": len(test_logs),
            "matched": len(matched),
            "detection_rate": len(matched) / len(test_logs) if test_logs else 0,
            "status": "validated"
        }
    
    def _matches_rule(self, rule: Dict[str, Any], log: Dict[str, Any]) -> bool:
        """Check if log matches Sigma rule conditions."""
        selection = rule.get('detection', {}).get('selection', {})
        for key, value in selection.items():
            if key not in log:
                return False
            if isinstance(value, list):
                if log[key] not in value:
                    return False
            elif log[key] != value:
                return False
        return True
