from unittest import TestCase

import docker


class TestCreateNetwork(TestCase):
    def test_create_network(self):
        client = docker.from_env()
        testnet = client.networks.create('test', driver='bridge')
        networks = client.networks.list()
        self.assertTrue(testnet in networks)
