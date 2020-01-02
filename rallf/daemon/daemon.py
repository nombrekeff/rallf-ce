import json
import os

import docker
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher
from rallf.model.tool import Tool
from rallf.model.robot import Robot
from rallf.model.task import Task
from rallf.network_manager import NetworkManager
from rallf.scheduler.device_scheduler import DeviceScheduler
from rallf.scheduler.task_scheduler import TaskScheduler


#   TODO:
#       * handle commands from cli (jsonrpc)
#       * manage data
#           * robots data (list of robots in directories)
#           * devices data (list of installed devices as docker images)
#       * ...
class Daemon:

    config_file = '../config/daemon.json'
    tasks_network_name = "rallf_tasks_network"
    devices_network_name = "rallf_devices_network"

    def __init__(self):
        file = self.config_file
        if not os.path.isfile(file): file += '.dist'
        with open(file, 'r') as f:
            config = json.load(f)
            self.robots = [Robot.load(r['id']) for r in config['robots']]
            self.devices = [Tool.load(d['id']) for d in config['devices']]
        client = docker.from_env()
        self.network_manager = NetworkManager(client)
        tasks_network = self.network_manager.create(self.tasks_network_name)
        devices_network = self.network_manager.create(self.devices_network_name)
        self.task_scheduler = TaskScheduler(docker.from_env(), tasks_network)
        self.device_scheduler = DeviceScheduler(docker.from_env(), devices_network)

    def persist(self):
        config = {
            'robots': self.robots,
            'devices': self.devices
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
        return [r for r in self.robots]

    def skill_train(self, img, robot: Robot) -> Task:
        t = Task(img=img)
        robot.learn(t)
        return t

    def skill_delete(self, skill: Task, robot: Robot) -> None:
        robot.forget(skill)
        self.task_scheduler.stop(skill)

    def skill_list(self, robot: Robot) -> list:
        return robot.skills[:]

    def device_install(self, img, driver, port) -> Tool:
        d = Tool(img=img)
        self.devices.append(d)
        return d

    def device_uninstall(self, device: Tool) -> None:
        self.devices.remove(device)

    def device_list(self, device: Tool) -> list:
        return self.devices[:]


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
