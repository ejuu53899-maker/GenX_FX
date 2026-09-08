"""Data models and schemas for GENX 3.6.9 Agent Operating System."""

from enum import IntEnum, Enum
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field


class PermissionLevel(IntEnum):
    """Agent Permission Levels."""
    LEVEL_0_READ_ONLY = 0
    LEVEL_1_ANALYZE = 1
    LEVEL_2_CREATE_FILES = 2
    LEVEL_3_DEPLOY = 3
    LEVEL_4_EXECUTE_ACTIONS = 4
    LEVEL_5_FINANCIAL_OPERATIONS = 5


class SystemState(str, Enum):
    """System Operating Modes."""
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    SAFE_MODE = "SAFE_MODE"
    EMERGENCY_STOP = "EMERGENCY_STOP"


class AgentMessage(BaseModel):
    """Inter-agent message format."""
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender: str
    receiver: str = "ALL"
    topic: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    level_required: PermissionLevel = PermissionLevel.LEVEL_0_READ_ONLY
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Task(BaseModel):
    """Task model for Commander and agent task queues."""
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    assigned_agent: str
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    required_level: PermissionLevel = PermissionLevel.LEVEL_1_ANALYZE
    parameters: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Dict[str, Any]] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Skill(BaseModel):
    """Skill capability package importable by agents or USB intelligence agent."""
    skill_id: str
    name: str
    version: str
    description: str
    required_level: PermissionLevel = PermissionLevel.LEVEL_1_ANALYZE
    author: str = "GENX_SYSTEM"
    code_or_handler: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Experience(BaseModel):
    """Learning loop experience model."""
    exp_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_name: str
    action: str
    result: Dict[str, Any]
    status: str  # SUCCESS, FAILURE, PARTIAL
    analysis: Optional[str] = None
    improvement_plan: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
