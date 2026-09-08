"""
GENX AI Memory System Skill Module
Manages short-term and long-term memory, trade journals, and lessons.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional

class MemoryEngine:
    """Core logic for GENX AI Memory System"""

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            # Default path relative to repository root
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
            self.journals_dir = os.path.join(base_dir, "data", "journals")
        else:
            self.journals_dir = data_dir

        os.makedirs(self.journals_dir, exist_ok=True)
        self.trades_file = os.path.join(self.journals_dir, "trades.json")
        self.decisions_file = os.path.join(self.journals_dir, "decisions.json")
        self.lessons_file = os.path.join(self.journals_dir, "lessons.json")

    def _load_json(self, filepath: str) -> List[Dict[str, Any]]:
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_json(self, filepath: str, data: List[Dict[str, Any]]) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def record_trade(self, trade_info: Dict[str, Any]) -> Dict[str, Any]:
        trades = self._load_json(self.trades_file)
        entry = {
            "timestamp": time.time(),
            "trade": trade_info
        }
        trades.append(entry)
        self._save_json(self.trades_file, trades)
        return {"status": "success", "recorded": entry}

    def record_decision(self, event: str, decision: str, reason: str, result: str, lesson: str) -> Dict[str, Any]:
        decisions = self._load_json(self.decisions_file)
        entry = {
            "timestamp": time.time(),
            "event": event,
            "decision": decision,
            "reason": reason,
            "result": result,
            "lesson": lesson
        }
        decisions.append(entry)
        self._save_json(self.decisions_file, decisions)

        if lesson:
            lessons = self._load_json(self.lessons_file)
            lessons.append({"timestamp": time.time(), "event": event, "lesson": lesson})
            self._save_json(self.lessons_file, lessons)

        return {"status": "success", "recorded": entry}

    def get_lessons(self) -> List[Dict[str, Any]]:
        return self._load_json(self.lessons_file)


def run(payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Skill entrypoint function"""
    engine = MemoryEngine()
    if not payload:
        return {"status": "success", "message": "Memory engine active.", "lessons": engine.get_lessons()}

    action = payload.get("action")
    if action == "record_decision":
        return engine.record_decision(
            event=payload.get("event", "general"),
            decision=payload.get("decision", "NONE"),
            reason=payload.get("reason", ""),
            result=payload.get("result", ""),
            lesson=payload.get("lesson", "")
        )
    elif action == "record_trade":
        return engine.record_trade(payload.get("trade_info", {}))
    elif action == "get_lessons":
        return {"status": "success", "lessons": engine.get_lessons()}

    return {"status": "success", "message": "Memory engine processed payload.", "data": payload}
