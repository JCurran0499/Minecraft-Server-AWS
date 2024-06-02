import boto3
import os
from datetime import datetime, timedelta
from dateutil import tz

ec2 = boto3.client('ec2', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')
invoker = boto3.client('lambda', region_name='us-east-1')

def lambda_handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')
    stop_function = os.environ.get('STOP_FUNCTION')
    period = os.environ.get('PERIOD')

    resp = ec2.describe_instances(InstanceIds=[instance_id])
    inst = resp['Reservations'][0]['Instances'][0]
    status = inst['State']['Name']
    
    start = inst['LaunchTime']
    now = datetime.now(tz.gettz('US/Eastern'))
    
    notify = False
    try:
        notify = event['queryStringParameters']['notify'] == "true"
    except:
        pass
    
    if notify and (status == "running") and (now > (start + timedelta(hours=int(period)))):
        msg = f"Your Minecraft server has been running for more than {period} hours. We have shut it down for you."
        sns.publish(TopicArn='arn:aws:sns:us-east-1:298451523862:Minecraft-Server-SNS', Message=msg)
        
        invoker.invoke(
            FunctionName=stop_function,
            InvocationType='Event'
        )

    if status == "running":
        status = status + " (" + inst['PublicIpAddress'] + ")"
    
    return {
        'statusCode': 200,
        'body': status
    }
    