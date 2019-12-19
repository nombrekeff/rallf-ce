from unittest import TestCase

from src.daemon.daemon import Daemon
from src.model.robot import Robot


class TestDaemon(TestCase):
    def test_start_daemon(self):
        daemon = Daemon()

    def test_store_and_load(self):
        daemon = Daemon()
        before = daemon.robot("ls")
        r = daemon.robot("create")
        self.assertIsInstance(r, Robot)
        daemon.persist()
        daemon2 = Daemon()
        after = daemon2.robot('ls')
        self.assertEqual(len(before) + 1, len(after))
        daemon2.robot("delete", robot=after[0])
        after2 = daemon2.robot('ls')
        self.assertEqual(len(before), len(after2))
        daemon2.persist()

    def test_delete_robot(self):
        daemon = Daemon()
        before = daemon.robot("ls")
        r = daemon.robot("create")
        daemon.robot("delete", robot=r)
        after = daemon.robot("ls")
        self.assertEqual(len(before), len(after))
