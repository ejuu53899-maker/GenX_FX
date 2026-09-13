"""
GENX Three-Layer Memory Architecture (v3.6.9)
Layer 1: Working Memory (ephemeral, session-only context)
Layer 2: Individual Long-Term Memory (agent-specific episodic/vector/knowledge base)
Layer 3: Shared Multi-Agent Memory (team coordination, task progress, system decisions, facts)
"""

import time
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    key: str
    content: Any
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentMemory(BaseModel):
    agent_id: str
    episodic: List[MemoryItem] = Field(default_factory=list)
    knowledge: Dict[str, MemoryItem] = Field(default_factory=dict)


class SharedMemory(BaseModel):
    tasks: Dict[str, MemoryItem] = Field(default_factory=dict)
    decisions: List[MemoryItem] = Field(default_factory=list)
    facts: Dict[str, MemoryItem] = Field(default_factory=dict)
    lessons_learned: List[MemoryItem] = Field(default_factory=list)


class ThreeLayerMemoryManager:
    """
    Manages Working, Individual Agent Long-Term, and Shared Multi-Agent Memory.
    """

    def __init__(self):
        self.working_memory: Dict[str, List[MemoryItem]] = {}
        self.agent_memories: Dict[str, AgentMemory] = {}
        self.shared_memory: SharedMemory = SharedMemory()

    # --- Layer 1: Working Memory (Ephemeral) ---
    def push_working_memory(self, session_id: str, key: str, content: Any) -> None:
        if session_id not in self.working_memory:
            self.working_memory[session_id] = []
        item = MemoryItem(key=key, content=content)
        self.working_memory[session_id].append(item)

    def get_working_memory(self, session_id: str) -> List[MemoryItem]:
        return self.working_memory.get(session_id, [])

    def clear_working_memory(self, session_id: str) -> None:
        if session_id in self.working_memory:
            del self.working_memory[session_id]

    # --- Layer 2: Individual Long-Term Memory ---
    def record_agent_experience(self, agent_id: str, key: str, content: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        if agent_id not in self.agent_memories:
            self.agent_memories[agent_id] = AgentMemory(agent_id=agent_id)
        item = MemoryItem(key=key, content=content, metadata=metadata or {})
        self.agent_memories[agent_id].episodic.append(item)

    def set_agent_knowledge(self, agent_id: str, key: str, content: Any) -> None:
        if agent_id not in self.agent_memories:
            self.agent_memories[agent_id] = AgentMemory(agent_id=agent_id)
        self.agent_memories[agent_id].knowledge[key] = MemoryItem(key=key, content=content)

    def get_agent_memory(self, agent_id: str) -> Optional[AgentMemory]:
        return self.agent_memories.get(agent_id)

    # --- Layer 3: Shared Multi-Agent Memory ---
    def record_shared_decision(self, key: str, decision: Any, agent_ids: List[str]) -> None:
        item = MemoryItem(key=key, content=decision, metadata={"participating_agents": agent_ids})
        self.shared_memory.decisions.append(item)

    def set_shared_fact(self, key: str, fact: Any) -> None:
        self.shared_memory.facts[key] = MemoryItem(key=key, content=fact)

    def get_shared_fact(self, key: str) -> Optional[Any]:
        item = self.shared_memory.facts.get(key)
        return item.content if item else None

    def record_lesson_learned(self, key: str, lesson: Any) -> None:
        item = MemoryItem(key=key, content=lesson)
        self.shared_memory.lessons_learned.append(item)
