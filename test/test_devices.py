from unittest import TestCase

import docker

from rallf.device_manager import DeviceManager
from rallf.scheduler.device_scheduler import DeviceScheduler


class TestDevices(TestCase):
    def test_install_firefox(self):
        dm = DeviceManager()
        client = docker.from_env()
        devices_network = client.networks.create('devices-network', driver='bridge')
        device_scheduler = DeviceScheduler(client, devices_network)
        img = 'selenium/standalone-firefox:latest'
        dm.install(img)
        dm.apply(device_scheduler)
        dm.uninstall(img)
        dm.apply(device_scheduler)
        self.assertTrue(True)
