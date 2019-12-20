from src.model.object import Object


class Task(Object):
    container = None
    img = None

    def __init__(self, img=None, id=None):
        super().__init__(id)
        self.img = img
