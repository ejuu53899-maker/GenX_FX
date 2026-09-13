"""
GENX AI Agent Router (v3.6.9)
Handles Intent Detection, Specialist Routing, Hierarchical Task Delegation, and Consensus Pattern Selection.
"""

from typing import Dict, List, Any, Optional
import logging
from src.agents.identity import AgentIdentity, AgentCard, PermissionLevel, AgentStatus

logger = logging.getLogger(__name__)


class RoutingPattern:
    SPECIALIST = "specialist_routing"
    HIERARCHICAL = "hierarchical_delegation"
    CONSENSUS = "multi_agent_consensus"


class AgentRouter:
    """
    Central Nervous System Router for GENX Agent Network.
    Registers agent identities, matches intents to agent capabilities, and decides orchestration pattern.
    """

    def __init__(self):
        self._registry: Dict[str, AgentCard] = {}

    def register_agent(self, card: AgentCard) -> None:
        """Register or update an agent card in the router database."""
        self._registry[card.identity.agent_id] = card
        logger.info(f"Registered agent {card.identity.agent_id} ({card.identity.role})")

    def get_agent(self, agent_id: str) -> Optional[AgentCard]:
        return self._registry.get(agent_id)

    def list_agents(self) -> List[AgentCard]:
        return list(self._registry.values())

    def detect_intent(self, user_prompt: str) -> str:
        """Simple intent detection based on key phrase analysis."""
        prompt_lower = user_prompt.lower()
        if any(kw in prompt_lower for kw in ["analyze", "chart", "market", "gold", "xauusd", "eurusd", "signal"]):
            return "market_analysis"
        elif any(kw in prompt_lower for kw in ["code", "build", "bug", "refactor", "python", "git"]):
            return "coding_task"
        elif any(kw in prompt_lower for kw in ["device", "vps", "minipc", "laptop", "cpu", "ram"]):
            return "device_management"
        elif any(kw in prompt_lower for kw in ["permission", "vault", "security", "guard", "token"]):
            return "security_audit"
        elif any(kw in prompt_lower for kw in ["mission", "start genx", "launch", "trading mission"]):
            return "mission_execution"
        return "general_query"

    def select_pattern(self, intent: str, high_risk: bool = False) -> str:
        """Select orchestration pattern based on task complexity/risk."""
        if high_risk:
            return RoutingPattern.CONSENSUS
        if intent in ["mission_execution"]:
            return RoutingPattern.HIERARCHICAL
        return RoutingPattern.SPECIALIST

    def route_request(self, user_prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Routes user query to appropriate agent(s) based on intent and pattern selection.
        """
        intent = self.detect_intent(user_prompt)
        high_risk = context.get("high_risk", False) if context else False
        pattern = self.select_pattern(intent, high_risk)

        # Match active agents capable of handling intent
        matching_agents = [
            card for card in self._registry.values()
            if intent in card.supported_intents and card.identity.status == AgentStatus.ACTIVE
        ]

        if not matching_agents:
            # Fallback to any active agent with generic capability
            matching_agents = [
                card for card in self._registry.values()
                if card.identity.status == AgentStatus.ACTIVE
            ]

        target_agent_ids = [card.identity.agent_id for card in matching_agents]

        return {
            "intent": intent,
            "pattern": pattern,
            "target_agent_ids": target_agent_ids,
            "prompt": user_prompt,
            "context": context or {}
        }
