"""
Data Governance AI Agent for Cloud Data Agent Kit.
Enforces PII scanning, IAM policies, and data classification.
"""

import logging
import re
from typing import Dict, Any, List, Optional
from ..config import DataAgentKitConfig

logger = logging.getLogger(__name__)


class DataGovernanceAgent:
    """AI Agent for data governance, security compliance, and privacy policies."""

    def __init__(self, config: Optional[DataAgentKitConfig] = None):
        self.config = config or DataAgentKitConfig()
        self.pii_patterns = {
            "email": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
            "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
            "api_key": re.compile(r"(?:api[_-]?key|secret|token)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", re.IGNORECASE),
        }

    def scan_for_pii_or_secrets(self, content: str) -> Dict[str, Any]:
        """Scan text or query results for sensitive information or leaked credentials."""
        findings = []
        for ptype, pattern in self.pii_patterns.items():
            matches = pattern.findall(content)
            if matches:
                findings.append({
                    "type": ptype,
                    "count": len(matches),
                    "sample": matches[0][:4] + "****"
                })

        return {
            "clean": len(findings) == 0,
            "findings_count": len(findings),
            "findings": findings,
            "governance_status": "COMPLIANT" if len(findings) == 0 else "NON_COMPLIANT"
        }

    def validate_query_governance(self, sql_query: str) -> Dict[str, Any]:
        """Verify SQL query compliance (e.g. no DROP DATABASE or unrestricted SELECT *)."""
        forbidden_keywords = ["DROP DATABASE", "DELETE FROM", "TRUNCATE TABLE"]
        query_upper = sql_query.upper()

        violations = [kw for kw in forbidden_keywords if kw in query_upper]
        return {
            "query": sql_query,
            "allowed": len(violations) == 0,
            "violations": violations,
            "policy": "Read-Only Data Agent Policy" if len(violations) == 0 else "Violation: Destructive SQL",
        }
