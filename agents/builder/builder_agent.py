"""Builder Agent - AI Software Engineer."""

import logging
from typing import Dict, Any
from agents.common.base_agent import BaseAgent
from agents.common.schemas import PermissionLevel, Task
from agents.common.message_bus import MessageBus

from .code_generator import CodeGenerator
from .tester import AutomatedTester
from .documentation import DocumentationGenerator
from .git_manager import GitManager
from .improvement_loop import ImprovementLoop

logger = logging.getLogger(__name__)


class BuilderAgent(BaseAgent):
    """Builder Agent responsible for code generation, testing, documentation, git management, and code improvements."""

    def __init__(self, message_bus: MessageBus):
        super().__init__(
            name="Builder",
            role="AI Software Engineer",
            default_permission=PermissionLevel.LEVEL_2_CREATE_FILES,
            message_bus=message_bus,
        )
        self.code_generator = CodeGenerator()
        self.tester = AutomatedTester()
        self.documentation = DocumentationGenerator()
        self.git_manager = GitManager()
        self.improvement_loop = ImprovementLoop()

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        """Execute Builder software engineering tasks."""
        action = task.parameters.get("action")
        if action == "GENERATE_CODE":
            class_name = task.parameters.get("class_name", "NewModule")
            methods = task.parameters.get("methods", ["execute"])
            code = self.code_generator.generate_class(class_name, methods)
            return {"status": "CODE_GENERATED", "code": code}

        elif action == "RUN_TESTS":
            test_path = task.parameters.get("test_path", "tests/")
            res = self.tester.run_tests(test_path)
            return res

        elif action == "GENERATE_DOC":
            mod_name = task.parameters.get("module", "Module")
            desc = task.parameters.get("description", "Auto-generated docs")
            doc = self.documentation.generate_doc(mod_name, desc, task.parameters)
            return {"status": "DOC_GENERATED", "documentation": doc}

        elif action == "GIT_COMMIT":
            msg = task.parameters.get("message", "Auto commit")
            return self.git_manager.commit_changes(msg)

        elif action == "PROPOSE_FIX":
            analysis = task.parameters.get("analysis", "No error details")
            return self.improvement_loop.propose_refactoring(analysis)

        return {"status": "COMPLETED", "message": f"Builder processed task '{task.title}'"}
