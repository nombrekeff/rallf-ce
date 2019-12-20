from src.model.object import Object
from src.model.task import Task


class Robot(Object):
    skills = []

    def __init__(self, id=None):
        super().__init__(id=None)
        self.home = None

    def learn(self, skill: Task):
        self.skills.append(skill)

    def forget(self, skill: Task):
        self.skills.remove(skill)
