"""
Unit tests for Device Network Controller.
"""

import time
import pytest
from src.network.device_controller import DeviceNetworkController, DeviceTelemetry


def test_device_network_controller():
    controller = DeviceNetworkController(heartbeat_timeout_sec=1.0)
    telemetry = DeviceTelemetry(
        device_id="NODE-01",
        device_type="Mini PC",
        os="Ubuntu 22.04"
    )
    controller.register_device(telemetry)

    health = controller.check_health()
    assert health["total_devices"] == 1
    assert health["online_count"] == 1

    # Simulate heartbeat update
    controller.update_heartbeat("NODE-01", cpu_percent=15.0, ram_percent=30.0)

    # Test remote command dispatch
    cmd_res = controller.dispatch_remote_command("NODE-01", "restart_service")
    assert cmd_res["status"] == "success"
