from src.model.robot import Robot
from src.model.task import Task
from src.scheduler.scheduler import Scheduler


class TaskScheduler:

    def start(self, task: Task, robot: Robot):
        volumes = {robot.home: {"bind": "/home/robot", "mode": "rw"}}
        container = self.docker.containers.run(task.img, name=task.id, detach=True, volumes=volumes)
        self.network.connect(container, alias=[task.id])
        task.container = container

    def stop(self, task: Task):
        task.container.kill()
