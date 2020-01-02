import docker
from werkzeug.serving import run_simple

from rallf.daemon.daemon import Daemon
from rallf.scheduler.scheduler import Scheduler

if __name__ == '__main__':
    scheduler = Scheduler(docker.from_env())
    daemon = Daemon()
    run_simple('localhost', 4000, daemon.application)
