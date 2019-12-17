import docker
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

from src.scheduler.scheduler import Scheduler

#   TODO:
#       * handle commands from cli (jsonrpc)
#       * manage data
#           * robots data (list of robots in directories)
#           * devices data (list of installed devices as docker images)
#       * ...


class Daemon:
    def __init__(self, task_manager, robot_manager, device_manager):
        self.device_manager = device_manager
        self.robot_manager = robot_manager
        self.scheduler = task_manager

    @dispatcher.add_method
    def login(self, **kwargs):
        return kwargs["foo"] + kwargs["bar"]

    @Request.application
    def application(self, request):
        # Dispatcher is dictionary {<method_name>: callable}
        dispatcher["echo"] = lambda s: s
        dispatcher["add"] = lambda a, b: a + b

        response = JSONRPCResponseManager.handle(
            request.data, dispatcher
        )
        return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    scheduler = Scheduler(docker.from_env())
    daemon = Daemon(scheduler, robot_manager, device_manager)
    run_simple('localhost', 4000, daemon.application)
