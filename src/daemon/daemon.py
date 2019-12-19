import json
import os
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

#   TODO:
#       * handle commands from cli (jsonrpc)
#       * manage data
#           * robots data (list of robots in directories)
#           * devices data (list of installed devices as docker images)
#       * ...
from src.model.device import Device
from src.model.robot import Robot
from src.model.task import Task


class Daemon:

    config_file = '../config/daemon.json'

    def __init__(self):
        # TODO:
        #   * load data from config volume
        file = self.config_file
        if not os.path.isfile(file): file += '.dist'
        with open(file, 'r') as f:
            config = json.load(f)
            self.robots = [Robot(r['id']) for r in config['robots']]
            self.devices = [Device(d['id']) for d in config['devices']]
            self.skills = [Task(t['id']) for t in config['skills']]

    def persist(self):
        config = {
            'robots': self.robots,
            'devices': self.devices,
            'skills': self.skills
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, default=lambda x: x.__dict__)

    def robot(self, action, robot=None, id=None):
        if action == "create":
            r = Robot()
            self.robots.append(r)
            return r
        elif action == "delete" and robot is not None:
            self.robots.remove(robot)
        elif action == "ls":
            return [r for r in self.robots]

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
