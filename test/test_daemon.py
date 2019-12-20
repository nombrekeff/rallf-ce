from unittest import TestCase

from src.daemon.daemon import Daemon
from src.model.robot import Robot


class TestDaemon(TestCase):

    def setUp(self) -> None:
        self.daemon = Daemon()

    def test_store_and_load(self):
        before = self.daemon.robot("ls")
        r = self.daemon.robot("create")
        self.assertIsInstance(r, Robot)
        self.daemon.persist()
        daemon2 = Daemon()
        after = daemon2.robot('ls')
        self.assertEqual(len(before) + 1, len(after))
        daemon2.robot("delete", robot=after[0])
        after2 = daemon2.robot('ls')
        self.assertEqual(len(before), len(after2))
        daemon2.persist()

    def test_delete_robot(self):
        before = self.daemon.robot("ls")
        r = self.daemon.robot("create")
        self.daemon.robot("delete", robot=r)
        after = self.daemon.robot("ls")
        self.assertEqual(len(before), len(after))


    def test_launch_and_stop_task(self):
        self.daemon.skill("create")