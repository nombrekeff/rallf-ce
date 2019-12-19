import uuid


class Robot:
    def __init__(self):
        self.id = str(uuid.uuid4())

    def __str__(self):
        return self.id


