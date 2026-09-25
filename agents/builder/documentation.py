"""Documentation Generator for Builder Agent."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class DocumentationGenerator:
    """Generates markdown documentation for code and modules."""

    def generate_doc(self, module_name: str, description: str, details: Dict[str, Any]) -> str:
        """Generate markdown documentation content."""
        doc = [
            f"# {module_name} Documentation",
            "",
            f"**Description:** {description}",
            "",
            "## Details",
        ]
        for k, v in details.items():
            doc.append(f"- **{k}**: {v}")
        return "\n".join(doc)
