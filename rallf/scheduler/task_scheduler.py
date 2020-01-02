from rallf.model.task import Task
from rallf.model.robot import Robot
from rallf.scheduler.scheduler import Scheduler


class TaskScheduler(Scheduler):

    def start(self, task: Task, robot: Robot):
        task_home = "%s/tasks/%s" % (robot.home, task.id)
        volumes = {task_home: {"bind": "/home/task", "mode": "rw"}}
        container = self.docker.containers.run(task.img, name=task.id, detach=True, volumes=volumes)
        self.network.connect(container, alias=[task.id])
        task.container = container

    def stop(self, task: Task):
        task.container.kill()
