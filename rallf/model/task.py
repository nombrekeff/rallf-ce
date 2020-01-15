from rallf.model.identifiable import Identifiable
from rallf.scheduler.scheduler import Scheduler


class Task(Identifiable):
    container = None
    img = None

    def __init__(self, task_scheduler: Scheduler, img=None, id=None):
        super().__init__(id)
        self.task_scheduler = task_scheduler
        self.img = img

    def run(self):
        pass