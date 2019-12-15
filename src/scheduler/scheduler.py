from docker import DockerClient


class Scheduler:
    def __init__(self, docker: DockerClient, network):
        self.network = network
        self.docker = docker

    def start(self, img):
        pass

    def stop(self, img):
        pass
