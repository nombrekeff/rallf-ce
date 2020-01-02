from docker import DockerClient
from docker.models.networks import Network


class Scheduler:
    def __init__(self, docker: DockerClient, network: Network):
        self.docker = docker
        self.network = network
