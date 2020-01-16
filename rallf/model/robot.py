from rallf.model.identifiable import Identifiable
from rallf.model.exportable import Exportable
from rallf.model.loadable import Loadable
from rallf.model.task import Task


class Robot(Identifiable, Loadable, Exportable):
    home = None
    skills = []

    def __init__(self):
        super().__init__()

    def load(self, config):
        pass

    def die(self):
        map(self.forget, self.skills)

    def learn(self, skill: Task):
        self.skills.append(skill)

    def forget(self, skill: Task):
        self.skills.remove(skill)
