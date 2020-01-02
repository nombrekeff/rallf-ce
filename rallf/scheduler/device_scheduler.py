from rallf.scheduler.scheduler import Scheduler


class DeviceScheduler(Scheduler):

    def start(self, img):
        dev = self.docker.containers.run(img, detach=True)
        self.network.connect(dev, aliases=[img])

    def stop(self, img):
        dev = self.docker.containers.get(img)
        dev.kill()
