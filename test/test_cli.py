import time
from unittest import TestCase

import docker

from src.cli.cli import RallfCLI


class TestCli(TestCase):
    def test_start_cli(self):
        client = docker.from_env()
        rallf = RallfCLI(client)
        rallf.start_incubator()
        time.sleep(1)
        rallf.stop_incubator()
        self.assertTrue(True)
