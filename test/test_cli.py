import time
from unittest import TestCase

import docker

from src.cli.cli import CLI


class TestCli(TestCase):
    def test_start_cli(self):
        client = docker.from_env()
        rallf = CLI(client)
        rallf.start_incubator()
        time.sleep(1)
        rallf.stop_incubator()
        self.assertTrue(True)
