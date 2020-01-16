from docker import DockerClient
from docker.models.networks import Network


class NetworkManager:
    def __init__(self, docker: DockerClient):
        self.docker = docker

    def create(self, name) -> Network:
        networks = self.docker.networks.list(names=[name])
        if len(networks) < 1:
            return self.docker.networks.create(name, driver='bridge', check_duplicate=True)
        return networks[0]

    def delete(self, network: Network):
        network.remove()
