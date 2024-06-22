import os
from datetime import datetime, timedelta
from dateutil import tz
from aws_lambda_powertools import Logger

domain = os.environ.get('DOMAIN')
period = os.environ.get('PERIOD')

logger = Logger()

RUNNING = "running"

START_MESSAGE = "Minecraft server is starting up, and in a few moments " + \
            "it will be accessible at " + domain + ". " + \
            "\nFor now, check the /status endpoint to " + \
            "track whether the server is up and running."

SHUTDOWN_MESSAGE = "Your Minecraft server has been running for more than " + \
            period + " hours. We have shut it down for you."

def server_expired(launch_time, status):
    now = datetime.now(tz.gettz('US/Eastern'))
    expir_time = launch_time + timedelta(hours=int(period))
    return (status.startswith("running")) and (now > expir_time)
