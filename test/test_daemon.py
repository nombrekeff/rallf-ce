from unittest import TestCase

from src.daemon.daemon import Daemon
from src.model.robot import Robot


class TestDaemon(TestCase):
    def test_start_daemon(self):
        daemon = Daemon()

    def test_create_robot(self):
        daemon = Daemon()
        res = daemon.robot("create")
        self.assertIsInstance(res, Robot)

    def test_delete_robot(self):
        daemon = Daemon()
        res = daemon.robot("create")
        daemon.robot("delete", id=res)
        robots = daemon.robot("ls")
        self.assertDictEqual({}, robots)
