import boto3
import os
import time
from domain.constants import logger, STARTUP_COMMAND

instance_id = os.environ.get('INSTANCE_ID')

class EC2Client:
    def __init__(self, region):
        self.client = boto3.client("ec2", region_name=region)
        self.ssm_client = boto3.client("ssm", region_name=region)

    def get_public_ip(self, wait=1):
        has_ip = False
        while not has_ip:
            logger.debug("Searching for public ip...")

            resp = self.client.describe_instances(InstanceIds=[instance_id])
            has_ip = ("PublicIpAddress" in resp['Reservations'][0]['Instances'][0])

            time.sleep(wait)

        return resp['Reservations'][0]['Instances'][0]['PublicIpAddress']
    
    def start_minecraft_server(self):
        logger.info("Starting the Minecraft server...")
        self.ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={
                'commands': [
                    "cd /opt/minecraft/server",
                    STARTUP_COMMAND
                ]
            }
        )
