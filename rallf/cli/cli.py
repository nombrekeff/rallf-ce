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
      rallf --help
      rallf --version

    Options:
      -e, --endpoint <docker_endpoint>   Docker endpoint to use [default: unix:///var/run/docker.sock]
      -u, --username <username>          rallf.com username
      -p, --password <password>          rallf.com password or - to get it from stdin [default: -]
      -r, --robot <robot>                Robot to use
      --persistent                       Keep the action persistent across restarts
      -h, --help                         Show this screen.
      -v, --version                      Show version.

    """
    version = 'Rallf CLI 0.0.1'

    config_volume = 'rallf_config'
    docker_endpoint = '/var/run/docker.sock'
    incubator_img = 'rallf/incubator:latest'
    daemon = None

    def __init__(self, client: DockerClient):
        self.docker = client
        self.docker.volumes.create(name=self.config_volume, driver='local')

    def cli(self, arg):
        if arg['incubator']:
            if arg['start']:
                print("Starting incubator", end=' ... ')
                self.start_incubator()
                print("[OK]")
                return
            if arg['stop']:
                print("Stopping incubator", end=' ... ')
                self.stop_incubator()
                print("[OK]")
                return
        else:
            print("NOT IMPLEMENTED")
            print(arg)

    def start_incubator(self):
        volumes = {
            self.config_volume: {'bind': '/config', 'mode': 'rw'},
            self.docker_endpoint: {'bind': '/var/run/docker.sock', 'mode': 'rw'},
        }
        ports = {'4000/tcp': 4000}
        self.docker.containers.run(
            self.incubator_img,
            name="incubator",
            detach=True,
            volumes=volumes,
            ports=ports,
            remove=True
        )

    def stop_incubator(self):
        daemon = self.docker.containers.get('incubator')
        if daemon is not None:
            daemon.kill()
