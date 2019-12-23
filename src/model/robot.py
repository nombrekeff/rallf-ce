from src.model.object import Object
from src.model.task import Task
from src.scheduler.task_scheduler import TaskScheduler


class Robot(Object):
    skills = []

    def __init__(self, scheduler: TaskScheduler, id=None):
        super().__init__(id=None)
        self.scheduler = scheduler
        self.home = None

    def die(self):
        for skill in self.skills:
            self.forget(skill)

    def learn(self, skill: Task):
        self.skills.append(skill)
        skill.start(self.scheduler, self)

    def forget(self, skill: Task):
        skill.stop()
        self.skills.remove(skill)
