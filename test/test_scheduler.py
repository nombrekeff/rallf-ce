from unittest import TestCase

import docker

from src.scheduler import Scheduler


class TestScheduler(TestCase):
    def test_test(self):
        client = docker.from_env()
        scheduler = Scheduler(client)
        scheduler.warmup()
