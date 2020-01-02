from docker import DockerClient


class CLI(object):
    """Rallf CLI.

    Usage:
      rallf login [--username <username>] [--password <password>]
      rallf incubator (start | stop) [--endpoint <docker_endpoint>] [--persistent]
      rallf robot ls
      rallf robot create
      rallf robot delete --robot <robot>
      rallf robot skill (learn | forget) <docker_image> --robot <robot>
      rallf robot device (add | remove) <docker_image> --robot <robot>
      rallf device (install | uninstall) <docker_image> [--driver <driver>] [--port <port>]
      rallf --help
      rallf --version

    Options:
      -e, --endpoint <docker_endpoint>   Docker endpoint to use [default: unix:///var/run/docker.sock]
      -u, --username <username>          rallf.com username
      -p, --password <password>          rallf.com password or - to get it from stdin [default: -]
      -r, --robot <robot>                Robot to use
      --persistent                       Keep the action persistent across restarts
      --port <port>                      TCP port to connect to, [default: 4444]
      -d, --driver <driver>              Driver name [default: selenium]
      -h, --help                         Show this screen.
      -v, --version                      Show version.

    """
    version = 'Rallf CLI 1.0'

    config_volume = 'rallf_config'
    docker_endpoint = '/var/run/docker.sock'
    incubator_img = 'rallf/incubator:latest'
    daemon = None

    def __init__(self, client: DockerClient):
        self.docker = client
        self.docker.volumes.create(name=self.config_volume, driver='local')

    def cli(self, arguments):
        print(arguments)

    def start_incubator(self):
        volumes = {
            self.config_volume: {'bind': '/config', 'mode': 'rw'},
            self.docker_endpoint: {'bind': '/var/run/docker.sock', 'mode': 'rw'},
        }
        ports = {'4000/tcp': 4000}
        self.daemon = self.docker.containers.run(
            self.incubator_img,
            detach=True,
            volumes=volumes,
            ports=ports,
            remove=True
        )

    def stop_incubator(self):
        if self.daemon is not None:
            self.daemon.kill()
