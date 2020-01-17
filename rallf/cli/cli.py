import getpass
import pathlib
import random
import sys

import yaml
import requests
from docker import DockerClient
from docker.errors import NotFound
from docker.models.containers import Container

from rallf.error.cli_error import CLIError
from rallf.error.rallf_error import RallfError
from rallf.error.rpc_error import RPCError


class CLI(object):
    """Rallf CLI.

    Usage:
      rallf login [--username <username>] [--password <password>]
      rallf incubator (start | stop) [--endpoint <docker_endpoint>] [--persistent] [--dev]
      rallf robot ls
      rallf robot create
      rallf robot delete --robot <robot>
      rallf robot skill (learn | forget) <docker_image> --robot <robot>
      rallf --help
      rallf --version

    Options:
      -e, --endpoint <docker_endpoint>   Docker endpoint to use [default: unix:///var/run/docker.sock]
      -u, --username <username>          rallf.com username
      -p, --password <password>          rallf.com password, use "-" to get it from stdin
      -r, --robot <robot>                Robot to use
      --persistent                       Keep the action persistent across restarts
      -d, --dev                          Run incubator in developer mode
      -h, --help                         Show this screen.
      -v, --version                      Show version.

    """
    version = 'Rallf CLI 0.0.1'

    config_volume = 'rallf_config'
    docker_endpoint = '/var/run/docker.sock'
    incubator_img = 'rallf/incubator:latest'
    url = "http://localhost:4000"
    daemon = None

    def __init__(self, client: DockerClient):
        self.docker = client
        self.docker.volumes.create(name=self.config_volume, driver='local')
        self.mapping = {
            "login": self.login,
            "incubator": {
                "start": self.start_incubator,
                "stop": self.stop_incubator,
            },
            "robot": {
                "ls": self.robot_list,
                "create": self.robot_create,
                "delete": self.robot_delete,
                "skill": {
                    "learn": self.learn_skill,
                    "forget": self.forget_skill,
                }
            }
        }

    def cli(self, arg, mapping=None):
        if mapping is None: mapping = self.mapping
        for command in mapping.keys():
            if command in arg and arg[command]:
                submapping = mapping[command]
                if isinstance(submapping, dict):
                    return self.cli(arg, submapping)
                else:
                    try:
                        print(submapping.__doc__, end="... ")
                        result = submapping(arg)
                        print("[OK]")
                        if isinstance(result, dict) and result == {}: return result
                        if isinstance(result, list) and result == []: return result
                        print(yaml.dump(result))
                        return result
                    except RallfError as e:
                        print("[ERROR] %s" % e)
                return

    def rpc_call(self, method, params=None):
        if params is None: params = {}
        request_id = random.randint(0, 100000000)
        payload = {
            "method": method,
            "params": params,
            "jsonrpc": 2.0,
            "id": request_id
        }
        response = requests.post(self.url, json=payload).json()
        assert response["id"] == request_id
        if "error" in response:
            raise RPCError(response["error"]["message"])
        assert "result" in response
        return response["result"]

    def login(self, arg):
        """Signing-in rallf.com"""
        self.get_incubator()
        username = arg["--username"] if arg["--username"] is not None else input("\nRALLF Username: ")
        password = arg["--password"] if arg["--password"] is not None else getpass.getpass("RALLF Password: ")
        password = sys.stdin.read().strip() if password == "-" else password
        return self.rpc_call("login", [{"username": username, "password": password}])

    def robot_list(self, arg):
        """Listing robots"""
        self.get_incubator()
        return self.rpc_call("robot_list")

    def robot_create(self, arg):
        """Creating robot"""
        self.get_incubator()
        return self.rpc_call("robot_create")

    def robot_delete(self, arg):
        """Deleting robot"""
        self.get_incubator()
        return self.rpc_call("delete_robot", arg["<robot>"])

    def learn_skill(self, arg):
        """Learning robot skill"""
        self.get_incubator()
        return self.rpc_call("learn_skill", arg["<robot>", "<docker_image>"])

    def forget_skill(self, arg):
        """Forgetting robot skill"""
        self.get_incubator()
        return self.rpc_call("forget_skill", arg["<robot>", "<docker_image>"])

    def start_incubator(self, arg):
        """Starting incubator"""
        volumes = {
            self.config_volume: {'bind': '/config', 'mode': 'rw'},
            self.docker_endpoint: {'bind': '/var/run/docker.sock', 'mode': 'rw'},
        }

        env = {}
        if arg["--dev"]:
            pwd = pathlib.Path().absolute()
            volumes[pwd] = {"bind": '/incubator', 'mode': 'ro'}
            env['DEBUG'] = "yes"
        ports = {'4000/tcp': 4000}

        try:
            self.docker.containers.get('incubator')
            raise CLIError("Incubator is already running")
        except NotFound:
            self.docker.containers.run(
                self.incubator_img,
                name="incubator",
                detach=True,
                volumes=volumes,
                environment=env,
                ports=ports,
                remove=True
            )

    def stop_incubator(self, arg):
        """Stopping incubator"""
        incubator = self.get_incubator()
        incubator.kill()

    def get_incubator(self) -> Container:
        try:
            return self.docker.containers.get('incubator')
        except NotFound:
            raise CLIError("Incubator is not running")
