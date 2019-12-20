from docker import DockerClient
from docker.models.networks import Network


class Scheduler:
    def __init__(self, docker: DockerClient, network: Network):
        self.docker = docker
        self.network = network

    def start(self, img):
        pass

    def stop(self, img):
        pass
