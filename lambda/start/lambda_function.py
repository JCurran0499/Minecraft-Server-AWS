import boto3
import os

ec2 = boto3.client('ec2', region_name='us-east-1')
invoker = boto3.client('lambda', region_name='us-east-1')

def lambda_handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')
    domain = os.environ.get('DOMAIN')
    dns_function = os.environ.get('DNS_FUNCTION')

    ec2.start_instances(InstanceIds=[instance_id])    
    
    invoker.invoke(
        FunctionName=dns_function,
        InvocationType='Event'
    )
    
    msg = 'Minecraft server is starting up, and in a few moments it will be ' + \
            'accessible at ' + domain + '. ' + \
            '\nFor now, check the /status endpoint to track whether the server is up and running.'
    return {
        'statusCode': 200,
        'body': msg
    }
