from src.model.task import Task
from src.scheduler.scheduler import Scheduler


class TaskScheduler(Scheduler):

    def start(self, task: Task):
        container = self.docker.containers.run(task.img, name=task.id, detach=True)
        self.network.connect(container, alias=[task.id])
        task.container = container

    def stop(self, task: Task):
        task.container.kill()
