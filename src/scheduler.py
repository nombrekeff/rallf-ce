
class Scheduler:
    def __init__(self, docker):
        self.docker = docker
        self.docker.networks.create('drivers', driver='ingress')
        self.docker.networks.create('tasks', driver='ingress')

    def warmup(self, task, robot):
        task = self.docker.containers.run(task, volumes=robot.get_home(task), detach=True)
        self.docker.networks.get('drivers').connect(task)
        self.docker.networks.get('tasks').connect(task)

    def cooldown(self, task):
        pass

    def run(self, task, routine):
        pass