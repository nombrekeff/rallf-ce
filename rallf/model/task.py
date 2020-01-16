from rallf.model.exportable import Exportable
from rallf.model.identifiable import Identifiable
from rallf.model.loadable import Loadable
from rallf.scheduler.scheduler import Scheduler


class Task(Identifiable, Loadable, Exportable):
    img = None

    def __init__(self, img=None, id=None):
        super().__init__(id)
        self.img = img

    def run(self):
        pass