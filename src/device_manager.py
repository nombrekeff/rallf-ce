from src.manager import Manager
from src.scheduler.scheduler import Scheduler


class DeviceManager(Manager):
    def __init__(self):
        self.to_install = []
        self.to_uninstall = []

    def install(self, docker_ref):
        if docker_ref in self.to_uninstall:
            self.to_uninstall.remove(docker_ref)
        elif docker_ref not in self.to_install:
            self.to_install.append(docker_ref)

    def uninstall(self, docker_ref):
        if docker_ref in self.to_install:
            self.to_install.remove(docker_ref)
        elif docker_ref in self.to_uninstall:
            self.to_uninstall.append(docker_ref)

    def apply(self, scheduler: Scheduler):
        for img in self.to_install:
            scheduler.start(img)
        for img in self.to_uninstall:
            scheduler.stop(img)
