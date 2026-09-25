"""Task Queue Manager for Commander Agent."""

import logging
from typing import List, Optional
from collections import deque
from agents.common.schemas import Task

logger = logging.getLogger(__name__)


class TaskQueue:
    """Queue for pending and active tasks across agents."""

    def __init__(self):
        self._pending_queue: deque[Task] = deque()
        self._completed_tasks: List[Task] = []
        self._failed_tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the queue."""
        self._pending_queue.append(task)
        logger.info(f"Task '{task.title}' ({task.task_id}) queued for agent '{task.assigned_agent}'.")

    def pop_next_task(self) -> Optional[Task]:
        """Get the next task in the queue."""
        if self._pending_queue:
            return self._pending_queue.popleft()
        return None

    def mark_completed(self, task: Task) -> None:
        """Record task as completed."""
        task.status = "COMPLETED"
        self._completed_tasks.append(task)

    def mark_failed(self, task: Task) -> None:
        """Record task as failed."""
        task.status = "FAILED"
        self._failed_tasks.append(task)

    def size(self) -> int:
        """Return pending queue size."""
        return len(self._pending_queue)
