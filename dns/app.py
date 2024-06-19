import boto3
import os
import time

from aws_lambda_powertools import Logger

logger = Logger()

ec2 = boto3.client('ec2', region_name='us-east-1')
route53 = boto3.client('route53', region_name='us-east-1')

instance_id = os.environ.get('INSTANCE_ID')
domain = os.environ.get('DOMAIN')
hosted_zone_id = os.environ.get('HOSTED_ZONE_ID')

def get_public_ip(wait=1):
    has_ip = False
    while not has_ip:
        logger.info("Searching for public ip...")

        resp = ec2.describe_instances(InstanceIds=[instance_id])
        has_ip = ("PublicIpAddress" in resp['Reservations'][0]['Instances'][0])

        time.sleep(wait)

    return resp['Reservations'][0]['Instances'][0]['PublicIpAddress']

@logger.inject_lambda_context
def handler(event, context):
    logger.info(
        "Initiating route53 record update...",
        instance_id=instance_id,
        domain=domain,
        hosted_zone_id=hosted_zone_id
    )

    public_ip = get_public_ip()
    
    logger.info(f"Updating route53 record with IP {public_ip}")
    route53.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain,
                        'Type': 'A',
                        'ResourceRecords': [
                            {
                                'Value': public_ip
                            }
                        ],
                        'TTL': 300
                    }
                }
            ]
        }
    )

    return {
        "status": "success"
    }

