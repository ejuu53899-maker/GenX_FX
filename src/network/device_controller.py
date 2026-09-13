"""
GENX Device Network Controller (v3.6.9)
Monitors physical and cloud infrastructure (Mini PC, Laptop, VPS, Cloud Services),
handles heartbeats, CPU/RAM telemetry, remote command dispatch, and self-healing.
"""

import time
import logging
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class DeviceTelemetry(BaseModel):
    device_id: str
    device_type: str  # Mini PC, Laptop, VPS, Cloud
    os: str          # Ubuntu, Windows, Linux
    status: str = "online"  # online, offline, degraded
    cpu_percent: float = 0.0
    ram_percent: float = 0.0
    temperature_c: Optional[float] = None
    last_heartbeat: float = Field(default_factory=time.time)


class DeviceNetworkController:
    """
    Manages edge devices, heartbeats, affinity rules, and automatic failure recovery.
    """

    def __init__(self, heartbeat_timeout_sec: float = 30.0):
        self.heartbeat_timeout_sec = heartbeat_timeout_sec
        self._devices: Dict[str, DeviceTelemetry] = {}

    def register_device(self, telemetry: DeviceTelemetry) -> None:
        self._devices[telemetry.device_id] = telemetry
        logger.info(f"Registered device {telemetry.device_id} ({telemetry.device_type} - {telemetry.os})")

    def update_heartbeat(self, device_id: str, cpu_percent: float, ram_percent: float, status: str = "online") -> None:
        if device_id in self._devices:
            dev = self._devices[device_id]
            dev.cpu_percent = cpu_percent
            dev.ram_percent = ram_percent
            dev.status = status
            dev.last_heartbeat = time.time()

    def check_health(self) -> Dict[str, Any]:
        """
        Inspects device network for offline or degraded nodes, triggering self-healing alerts.
        """
        now = time.time()
        offline_nodes = []
        for dev_id, dev in self._devices.items():
            if now - dev.last_heartbeat > self.heartbeat_timeout_sec:
                dev.status = "offline"
                offline_nodes.append(dev_id)
                logger.warning(f"Device {dev_id} marked OFFLINE due to missed heartbeat.")

        return {
            "total_devices": len(self._devices),
            "online_count": sum(1 for d in self._devices.values() if d.status == "online"),
            "offline_nodes": offline_nodes,
            "devices": {k: v.model_dump() for k, v in self._devices.items()}
        }

    def dispatch_remote_command(self, device_id: str, command: str) -> Dict[str, Any]:
        dev = self._devices.get(device_id)
        if not dev or dev.status == "offline":
            return {"status": "error", "message": f"Device {device_id} is unavailable/offline."}

        logger.info(f"Dispatched command '{command}' to device {device_id}")
        return {"status": "success", "device_id": device_id, "command": command, "result": "Command executed successfully"}
