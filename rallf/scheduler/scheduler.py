from docker import DockerClient
from docker.models.containers import Container
from docker.models.networks import Network

from rallf.model.robot import Robot
from rallf.model.task import Task


class Scheduler:
    network = None
    docker = None
    running_tasks = []

    def __init__(self, docker: DockerClient, network: Network):
        self.docker = docker
        self.network = network

    def start(self, task: Task, robot: Robot):
        task_home = "%s/tasks/%s" % (robot.home, task.id)
        volumes = {task_home: {"bind": "/home/task", "mode": "rw"}}
        container = self.docker.containers.run(task.img, name=task.id, detach=True, volumes=volumes)
        self.network.connect(container, alias=[task.id])
        self.running_tasks.append(container)
        return container

    def stop(self, container: Container):
        container.kill()
