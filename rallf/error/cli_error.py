from rallf.error.rallf_error import RallfError


class CLIError(RallfError):
    def __init__(self, message):
        super().__init__("cli: %s" % message)
