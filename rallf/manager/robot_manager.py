from rallf.model.exportable import Exportable
from rallf.model.loadable import Loadable
from rallf.model.robot import Robot


class RobotManager(Loadable, Exportable):

    def __init__(self, robots: dict):
        self.robots = robots

    def load(self, config):
        self.robots = [{r.id: r} for r in [Robot.load(c) for c in config]]

    def create(self):
        r = Robot()
        self.robots[r.id] = r
        return r

    def delete(self, robot_id: str):
        r = self.robots[robot_id]
        del self.robots[robot_id]
        r.die()
