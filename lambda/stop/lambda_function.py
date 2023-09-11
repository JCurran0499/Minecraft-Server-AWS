import boto3
import os

ec2 = boto3.client('ec2', region_name='us-east-1')

def lambda_handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')

    ec2.stop_instances(InstanceIds=[instance_id])
    return {
        'statusCode': 200,
        'body': 'Minecraft server has been stopped'
    }
