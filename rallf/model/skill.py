from rallf.model.robot import Robot
from rallf.model.task import Task
from rallf.scheduler.scheduler import Scheduler


class Skill(Task):
    container = None
    img = None

    def __init__(self, img=None, id=None):
        super().__init__(id)
        self.img = img

    def start(self, scheduler: Scheduler, robot: Robot):
        scheduler.start(self, robot)
