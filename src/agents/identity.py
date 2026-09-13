"""
GENX AI Agent Identity & Capability Manifest Model (v3.6.9)
Manages agent unique identity, role, permissions, status, and capability card (A2A protocol).
"""

from enum import Enum, IntEnum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PermissionLevel(IntEnum):
    LEVEL_0_OBSERVE = 0      # Observe only
    LEVEL_1_ANALYZE = 1      # Analyze
    LEVEL_2_RECOMMEND = 2    # Recommend
    LEVEL_3_APPROVAL = 3     # Execute with approval
    LEVEL_4_AUTONOMOUS = 4   # Autonomous execution


class AgentStatus(str, Enum):
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


class AgentIdentity(BaseModel):
    agent_id: str
    name: str
    role: str
    permission_level: PermissionLevel = PermissionLevel.LEVEL_1_ANALYZE
    status: AgentStatus = AgentStatus.ACTIVE
    capabilities: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentCard(BaseModel):
    """
    Agent Capability Card for Agent-to-Agent (A2A) Discovery
    """
    identity: AgentIdentity
    protocol: str = "A2A_v1"
    supported_intents: List[str] = Field(default_factory=list)
    endpoint: Optional[str] = None
