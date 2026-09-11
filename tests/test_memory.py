"""
Unit tests for GENX Three-Layer Memory Core.
"""

import pytest
from src.memory.manager import ThreeLayerMemoryManager


def test_three_layer_memory():
    mem = ThreeLayerMemoryManager()

    # Layer 1: Working Memory
    mem.push_working_memory("session_101", "query", "What is gold price?")
    items = mem.get_working_memory("session_101")
    assert len(items) == 1
    assert items[0].content == "What is gold price?"

    # Layer 2: Agent Memory
    mem.record_agent_experience("GENX-TRADER-001", "trade_1", {"symbol": "XAUUSD", "profit": 150})
    agent_mem = mem.get_agent_memory("GENX-TRADER-001")
    assert agent_mem is not None
    assert len(agent_mem.episodic) == 1

    # Layer 3: Shared Memory
    mem.record_shared_decision("dec_1", "APPROVED BUY XAUUSD", ["GENX-TRADER-001", "GENX-SECURITY-001"])
    mem.set_shared_fact("daily_drawdown", 0.004)
    assert mem.get_shared_fact("daily_drawdown") == 0.004
