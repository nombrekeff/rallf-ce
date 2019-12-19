import json

import docker
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

#   TODO:
#       * handle commands from cli (jsonrpc)
#       * manage data
#           * robots data (list of robots in directories)
#           * devices data (list of installed devices as docker images)
#       * ...
from src.model.robot import Robot


class Daemon:

    config_file = '../config/daemon.json'

    def __init__(self):
        # TODO:
        #   * load data from config volume
        with open(self.config_file, 'r') as f:
            config = json.load(f)
            self.robots = config['robots']
            self.devices = config['devices']

    def persist(self):
        config = {
            'robots': self.robots,
            'devices': self.devices
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def robot(self, action, id=None):
        if action == "create":
            robot = Robot()
            self.robots[id] = robot
            return robot
        elif action == "delete" and id is not None:
            if id in self.robots.keys():
                del self.robots[id]
        elif action == "ls":
            return self.robots

    @dispatcher.add_method
    def robot_rpc(self, **kwargs):
        return kwargs["username"] + kwargs["password"]

    @dispatcher.add_method
    def login(self, **kwargs):
        return kwargs["username"] + kwargs["password"]

    @Request.application
    def application(self, request):
        # Dispatcher is dictionary {<method_name>: callable}
        dispatcher["echo"] = lambda s: s
        dispatcher["add"] = lambda a, b: a + b

        response = JSONRPCResponseManager.handle(
            request.data, dispatcher
        )
        return Response(response.json, mimetype='application/json')
