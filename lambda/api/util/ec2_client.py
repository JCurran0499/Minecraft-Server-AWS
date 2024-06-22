import boto3
import os
from domain.constants import logger, RUNNING

instance_id = os.environ.get('INSTANCE_ID')
domain = os.environ.get('DOMAIN')

class EC2Client:
    def __init__(self, region):
        self.client = boto3.client("ec2", region_name=region)

    def start_server(self):
        logger.info(f"Starting server {instance_id}...")
        return self.client.start_instances(InstanceIds=[instance_id])
    
    def stop_server(self):
        logger.info(f"Stopping server {instance_id}!")
        return self.client.stop_instances(InstanceIds=[instance_id])
    
    def get_server_status(self):
        logger.info(f"Getting status for server {instance_id}...")
        resp = self.client.describe_instances(InstanceIds=[instance_id])
        inst = resp['Reservations'][0]['Instances'][0]

        status = inst['State']['Name']
        launch_time = inst['LaunchTime']

        if status == RUNNING:
            status = f"{status} ({inst['PublicIpAddress']})"
        
        return (launch_time,status)
    