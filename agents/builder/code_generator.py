"""Code Generator for Builder Agent."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class CodeGenerator:
    """Generates Python source code and skill templates."""

    def generate_class(self, class_name: str, methods: list) -> str:
        """Generate code template for a class."""
        code = [f"class {class_name}:", f'    """Generated class {class_name}."""', ""]
        for m in methods:
            code.append(f"    def {m}(self):")
            code.append(f'        """Method {m}."""')
            code.append("        pass")
            code.append("")
        return "\n".join(code)

    def generate_skill_package(self, skill_id: str, name: str, code: str) -> Dict[str, Any]:
        """Wrap source code into a skill package dictionary."""
        return {
            "skill_id": skill_id,
            "name": name,
            "code": code,
            "version": "1.0.0",
        }
