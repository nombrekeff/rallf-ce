import json
import os

import docker
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

from rallf.manager.network_manager import NetworkManager
from rallf.scheduler.scheduler import Scheduler
from rallf.model.robot import Robot
from rallf.model.task import Task


#   TODO:
#       * handle commands from cli (jsonrpc)
#       * manage data
#           * robots data (list of robots in directories)
#           * devices data (list of installed devices as docker images)
#       * ...
class Daemon:

    config_file = '../config/daemon.json'
    tasks_network_name = "rallf_tasks_network"

    def __init__(self):
        file = self.config_file
        if not os.path.isfile(file): file += '.dist'
        with open(file, 'r') as f:
            config = json.load(f)
            self.robots = [Robot.load(r['id']) for r in config['robots']]
        client = docker.from_env()
        self.network_manager = NetworkManager(client)
        tasks_network = self.network_manager.create(self.tasks_network_name)

        self.scheduler = Scheduler(client, tasks_network)

    def persist(self):
        config = {
            'robots': self.robots,
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, default=lambda x: x.__dict__)

    def robot_create(self) -> Robot:
        r = Robot()
        self.robots.append(r)
        return r

    def robot_delete(self, robot: Robot):
        robot.die()
        self.robots.remove(robot)

    def robot_list(self):
        return self.robots[:]

    def skill_train(self, img, robot: Robot) -> Task:
        t = Task(img=img)
        robot.learn(t)
        return t

    def skill_delete(self, skill: Task, robot: Robot) -> None:
        robot.forget(skill)
        self.scheduler.stop(skill)

    def skill_list(self, robot: Robot) -> list:
        return robot.skills[:]


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
