from rallf.model.robot import Robot
from rallf.model.task import Task
from rallf.scheduler.task_scheduler import TaskScheduler


class Skill(Task):
    container = None
    img = None

    def __init__(self, img=None, id=None):
        super().__init__(id)
        self.img = img

    def start(self, scheduler: TaskScheduler, robot: Robot):
        scheduler.start(self, robot)
