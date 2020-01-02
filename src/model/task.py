from src.model.identifiable import Identifiable
from src.scheduler.task_scheduler import TaskScheduler


class Task(Identifiable):
    container = None
    img = None

    def __init__(self, task_scheduler: TaskScheduler, img=None, id=None):
        super().__init__(id)
        self.task_scheduler = task_scheduler
        self.img = img

    def run(self):
        pass