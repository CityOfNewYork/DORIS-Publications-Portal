import subprocess

from flask_script import Manager, Server

from app import create_app
from config import DEV

manager = Manager(create_app(DEV))


class ServerWithRedis(Server):
    """
    Same as flask_script.Server but
    also starts redis if not running.

    """
    def __init__(self):
        super(ServerWithRedis, self).__init__()
        try:
            subprocess.check_output(['pgrep', 'redis'])
        except subprocess.CalledProcessError:
            print("Starting Redis...")
            subprocess.call(['./run_redis.sh'])
            print("Done.")


manager.add_command("runserver", ServerWithRedis())

if __name__ == "__main__":
    manager.run()
