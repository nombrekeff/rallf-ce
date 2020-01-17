from rallf.error.rallf_error import RallfError


class RPCError(RallfError):
    def __init__(self, message):
        super().__init__("rpc: %s" % message)
