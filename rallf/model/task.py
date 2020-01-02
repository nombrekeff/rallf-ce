from rallf.model.identifiable import Identifiable
from rallf.scheduler.task_scheduler import TaskScheduler


class Task(Identifiable):
    container = None
    img = None

    def __init__(self, task_scheduler: TaskScheduler, img=None, id=None):
        super().__init__(id)
        self.task_scheduler = task_scheduler
        self.img = img

    def run(self):
        pass