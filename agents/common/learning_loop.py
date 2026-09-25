"""Agent Learning Loop Manager - Experience, Failure Analysis, & Skill Evolution."""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from .schemas import Experience, Skill

logger = logging.getLogger(__name__)


class LearningLoopManager:
    """Manages the learning loop: ACTION -> RESULT -> LOG -> ANALYSIS -> IMPROVEMENT -> NEW SKILL VERSION."""

    def __init__(self, data_dir: Path = Path("data")):
        self.data_dir = data_dir
        self.memories_dir = data_dir / "memories"
        self.experiences_dir = data_dir / "experiences"
        self.failures_dir = data_dir / "failures"
        self.improvements_dir = data_dir / "improvements"

        for d in [self.memories_dir, self.experiences_dir, self.failures_dir, self.improvements_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def log_experience(self, exp: Experience) -> Path:
        """Log experience to JSON file in data/experiences/."""
        filepath = self.experiences_dir / f"exp_{exp.exp_id}.json"
        filepath.write_text(json.dumps(exp.model_dump(), indent=2), encoding="utf-8")
        logger.info(f"Logged experience '{exp.exp_id}' for agent '{exp.agent_name}' ({exp.status})")

        if exp.status == "FAILURE":
            self._log_failure(exp)
        else:
            self._log_memory(exp)

        return filepath

    def _log_failure(self, exp: Experience) -> Path:
        """Log failure analysis record in data/failures/."""
        fail_file = self.failures_dir / f"failure_{exp.exp_id}.json"
        fail_data = {
            "exp_id": exp.exp_id,
            "agent_name": exp.agent_name,
            "action": exp.action,
            "error_result": exp.result,
            "analysis": exp.analysis or "Failure encountered during execution.",
            "timestamp": exp.timestamp,
        }
        fail_file.write_text(json.dumps(fail_data, indent=2), encoding="utf-8")
        logger.warning(f"Logged failure record to '{fail_file}'")
        return fail_file

    def _log_memory(self, exp: Experience) -> Path:
        """Log successful memory record in data/memories/."""
        mem_file = self.memories_dir / f"memory_{exp.exp_id}.json"
        mem_data = {
            "exp_id": exp.exp_id,
            "agent_name": exp.agent_name,
            "action": exp.action,
            "result": exp.result,
            "timestamp": exp.timestamp,
        }
        mem_file.write_text(json.dumps(mem_data, indent=2), encoding="utf-8")
        return mem_file

    def generate_improvement_plan(self, exp_id: str) -> Optional[Dict[str, Any]]:
        """Analyze a failure and generate an improvement plan in data/improvements/."""
        fail_file = self.failures_dir / f"failure_{exp_id}.json"
        if not fail_file.exists():
            logger.error(f"Failure record '{exp_id}' not found.")
            return None

        fail_data = json.loads(fail_file.read_text(encoding="utf-8"))
        imp_file = self.improvements_dir / f"improvement_{exp_id}.json"
        imp_data = {
            "exp_id": exp_id,
            "agent_name": fail_data["agent_name"],
            "original_action": fail_data["action"],
            "improvement": f"Adjust logic/parameters for {fail_data['action']} based on analysis: {fail_data['analysis']}",
            "recommended_version_bump": "1.0.1",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        imp_file.write_text(json.dumps(imp_data, indent=2), encoding="utf-8")
        logger.info(f"Generated improvement plan at '{imp_file}'")
        return imp_data

    def evolve_skill(self, current_skill: Skill, new_version: str, improvement_details: str) -> Skill:
        """Evolve an existing skill to a new version based on learning loop improvement."""
        evolved_skill = Skill(
            skill_id=f"{current_skill.skill_id}_v{new_version.replace('.', '_')}",
            name=current_skill.name,
            version=new_version,
            description=f"{current_skill.description} (Evolved: {improvement_details})",
            required_level=current_skill.required_level,
            author=f"{current_skill.author}_LEARNING_LOOP",
            code_or_handler=current_skill.code_or_handler,
            metadata={"evolved_from": current_skill.version, "improvement": improvement_details},
        )
        logger.info(f"Skill '{current_skill.name}' evolved to v{new_version}")
        return evolved_skill
