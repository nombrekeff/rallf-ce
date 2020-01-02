import uuid


class Identifiable:
    def __init__(self, id=None):
        self.id = str(uuid.uuid4()) if id is None else id

    def __str__(self):
        return self.id

    def load(self, src):
        pass