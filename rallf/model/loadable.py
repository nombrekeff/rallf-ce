from abc import abstractmethod


class Loadable:

    @abstractmethod
    def load(self, config):
        pass
