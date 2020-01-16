from unittest import TestCase

from rallf.daemon.daemon import Daemon
from rallf.model.robot import Robot


class TestDaemon(TestCase):

    def setUp(self) -> None:
        self.daemon = Daemon()

    def test_store_and_load(self):
        before = self.daemon.robot_list()
        r = self.daemon.robot_create()
        self.assertIsInstance(r, Robot)
        self.daemon.export()
        daemon2 = Daemon()
        after = daemon2.robot_list()
        self.assertEqual(len(before) + 1, len(after))
        daemon2.robot_delete(robot=after[0])
        after2 = daemon2.robot_list()
        self.assertEqual(len(before), len(after2))
        daemon2.export()

    def test_delete_robot(self):
        before = self.daemon.robot_list()
        r = self.daemon.robot_create()
        self.daemon.robot_delete(robot=r)
        after = self.daemon.robot_list()
        self.assertEqual(len(before), len(after))


    def test_launch_and_stop_task(self):
        robot = self.daemon.robots[0]
        robot.train('')