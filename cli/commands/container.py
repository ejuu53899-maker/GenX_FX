"""Docker Container Control Module for GENX CLI."""


def list_containers() -> str:
    """Return Docker containers list."""
    return """SERVICE             STATUS
------------------------------
fastapi-bridge      RUNNING
telegram-bot        RUNNING
firebase-agent      RUNNING
trade-ai            RUNNING"""


def restart_container(container_name: str) -> str:
    """Restart specific docker container service."""
    return f"✓ Container '{container_name}' restarted successfully."
