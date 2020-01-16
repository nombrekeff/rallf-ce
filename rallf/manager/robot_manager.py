from rallf.model.exportable import Exportable
from rallf.model.loadable import Loadable
from rallf.model.robot import Robot


class RobotManager(Loadable, Exportable):

    def __init__(self, config):
        self.robots = [Robot.load(r) for r in config]

    def create(self):
        r = Robot()
        self.robots.append(r)
        return r

    def delete(self, robot: Robot):
        self.robots.remove(robot)
        robot.die()