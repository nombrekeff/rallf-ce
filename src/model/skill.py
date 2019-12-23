from src.model.robot import Robot
from src.model.task import Task
from src.scheduler.task_scheduler import TaskScheduler


class Skill(Task):
    container = None
    img = None

    def __init__(self, img=None, id=None):
        super().__init__(id)
        self.img = img

    def start(self, scheduler: TaskScheduler, robot: Robot):
        scheduler.start(self, robot)
