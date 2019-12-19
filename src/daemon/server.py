import docker
from werkzeug.serving import run_simple

from src.daemon.daemon import Daemon
from src.scheduler.scheduler import Scheduler

if __name__ == '__main__':
    scheduler = Scheduler(docker.from_env())
    daemon = Daemon()
    run_simple('localhost', 4000, daemon.application)
