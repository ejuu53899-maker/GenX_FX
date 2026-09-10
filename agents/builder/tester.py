"""Tester for Builder Agent."""

import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AutomatedTester:
    """Executes automated test suites and reports test results."""

    def run_tests(self, test_path: str = "tests/") -> Dict[str, Any]:
        """Run pytest on specified directory or file."""
        logger.info(f"Running pytest on '{test_path}'...")
        try:
            res = subprocess.run(
                ["python3", "-m", "pytest", test_path],
                capture_output=True,
                text=True,
                timeout=60,
            )
            passed = res.returncode == 0
            return {
                "passed": passed,
                "returncode": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr,
            }
        except Exception as e:
            logger.error(f"Test execution error: {e}")
            return {"passed": False, "error": str(e)}
