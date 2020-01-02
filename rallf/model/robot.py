from rallf.model.tool import Tool
from rallf.model.identifiable import Identifiable
from rallf.model.task import Task


class Robot(Identifiable):
    home = None
    skills = []
    tools = []

    def __init__(self):
        super().__init__()

    def die(self):
        for skill in self.skills: self.forget(skill)
        for tool in self.tools: self.throw(tool)

    def learn(self, skill: Task):
        self.skills.append(skill)

    def forget(self, skill: Task):
        self.skills.remove(skill)

    def use(self, tool: Tool):
        self.tools.append(tool)

    def throw(self, tool: Tool):
        self.tools.remove(tool)

    def load(self, src):
        pass