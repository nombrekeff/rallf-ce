import json
import os

import docker
from docker import DockerClient
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

from rallf.manager.network_manager import NetworkManager
from rallf.manager.robot_manager import RobotManager
from rallf.model.exportable import Exportable
from rallf.model.loadable import Loadable
from rallf.scheduler.scheduler import Scheduler
from rallf.model.robot import Robot
from rallf.model.task import Task


#   TODO:
#       * handle commands from cli (jsonrpc)
#       * manage data
#           * robots data (list of robots in directories)
#           * devices data (list of installed devices as docker images)
#       * ...
class Daemon(Loadable, Exportable):

    config_file = 'config/daemon.json'
    tasks_network_name = "rallf_tasks_network"
    robot_manager = None

    def __init__(self, scheduler: Scheduler):
        file = self.config_file
        if not os.path.isfile(file): file += '.dist'
        with open(file, 'r') as f:
            config = json.load(f)
            self.load(config)

        self.scheduler = scheduler

    def load(self, config):
        self.robot_manager = RobotManager(config['robots'])

    def export(self):
        config = {
            'robots': self.robot_manager.export(),
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, default=lambda x: x.__dict__)

    def robot_create(self) -> Robot:
        return self.robot_manager.create()

    def robot_delete(self, robot: Robot):
        self.robot_manager.delete(robot)

    def robot_list(self):
        return self.robot_manager.robots[:]

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
    def echo2(self, **kwargs):
        return kwargs

    @Request.application
    def application(self, request):
        # Dispatcher is dictionary {<method_name>: callable}
        dispatcher["login"] = lambda s: "Login successful"
        dispatcher["echo"] = lambda s: s
        dispatcher["add"] = lambda a, b: a + b

        response = JSONRPCResponseManager.handle(
            request.data, dispatcher
        )
        return Response(response.json, mimetype='application/json')
