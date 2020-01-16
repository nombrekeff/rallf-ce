from docker import DockerClient
from docker.models.containers import Container

from rallf.manager.network_manager import NetworkManager
from rallf.model.robot import Robot
from rallf.model.task import Task


class Scheduler:
    running_tasks = []

    def __init__(self, docker: DockerClient, network_manager: NetworkManager):
        self.docker = docker
        self.network_manager = network_manager

    def start(self, task: Task, robot: Robot):
        task_home = "%s-%s" % (robot, task)
        volumes = {task_home: {"bind": "/workspace", "mode": "rw"}}
        container = self.docker.containers.run(task.img, name=task.id, detach=True, volumes=volumes)
        network = self.network_manager.create("%s-%s" % (robot, task))
        network.connect(container, alias=[task.id])
        self.running_tasks.append(container)
        return container

    def stop(self, container: Container):
        container.kill()
