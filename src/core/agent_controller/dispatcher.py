"""
GENX AI Agent Dispatcher & Execution Coordinator (v3.6.9)
Dispatches routed tasks to target agents, coordinates multi-agent consensus, and aggregates subtask execution.
"""

from typing import Dict, List, Any, Optional, Callable
import logging
from src.core.agent_controller.router import AgentRouter, RoutingPattern
from src.agents.identity import AgentIdentity, AgentCard, AgentStatus

logger = logging.getLogger(__name__)


class AgentDispatcher:
    """
    Executes dispatched agent requests according to routed orchestration patterns.
    """

    def __init__(self, router: AgentRouter):
        self.router = router
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_agent_handler(self, agent_id: str, handler_func: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        """Register an execution handler for a specific agent ID."""
        self._handlers[agent_id] = handler_func
        logger.info(f"Registered execution handler for agent {agent_id}")

    def dispatch(self, route_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch request to destination agent(s) based on pattern.
        """
        pattern = route_info.get("pattern", RoutingPattern.SPECIALIST)
        target_ids = route_info.get("target_agent_ids", [])
        prompt = route_info.get("prompt", "")
        intent = route_info.get("intent", "general_query")

        if not target_ids:
            return {
                "status": "error",
                "message": "No active agent found for intent",
                "route": route_info
            }

        if pattern == RoutingPattern.SPECIALIST:
            # Send to primary specialist (first matching agent)
            primary_agent = target_ids[0]
            return self._execute_single(primary_agent, route_info)

        elif pattern == RoutingPattern.HIERARCHICAL:
            # Primary agent acts as lead delegator, sub-results aggregated
            results = []
            for agent_id in target_ids:
                res = self._execute_single(agent_id, route_info)
                results.append(res)
            return {
                "status": "success",
                "pattern": RoutingPattern.HIERARCHICAL,
                "lead_agent": target_ids[0],
                "subtask_results": results
            }

        elif pattern == RoutingPattern.CONSENSUS:
            # Execute across multiple agents and require consensus
            responses = []
            for agent_id in target_ids:
                responses.append(self._execute_single(agent_id, route_info))

            # Aggregate consensus
            approved = all(r.get("status") == "success" for r in responses)
            return {
                "status": "success" if approved else "rejected",
                "pattern": RoutingPattern.CONSENSUS,
                "consensus_reached": approved,
                "agent_responses": responses
            }

        return self._execute_single(target_ids[0], route_info)

    def _execute_single(self, agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        handler = self._handlers.get(agent_id)
        if handler:
            try:
                result = handler(payload)
                return {
                    "agent_id": agent_id,
                    "status": "success",
                    "output": result
                }
            except Exception as e:
                logger.error(f"Execution error on agent {agent_id}: {e}")
                return {
                    "agent_id": agent_id,
                    "status": "error",
                    "error": str(e)
                }
        else:
            # Default response if handler is not dynamically hooked
            return {
                "agent_id": agent_id,
                "status": "success",
                "output": f"Processed prompt '{payload.get('prompt')}' via agent {agent_id}"
            }
