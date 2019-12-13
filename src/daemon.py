import docker
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

from src.scheduler import Scheduler


class Daemon:
    def __init__(self):
        docker_client = docker.from_env()
        scheduler = Scheduler(docker_client)

    @dispatcher.add_method
    def foobar(self, **kwargs):
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
    run_simple('localhost', 4000, Daemon().application)
