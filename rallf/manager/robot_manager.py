from rallf.model.robot import Robot


class RobotManager:
    robots = []

    def create(self):
        r = Robot()
        self.robots.append(r)
        return r

    def delete(self, robot: Robot):
        self.robots.remove(robot)
        robot.die()