import boto3
import os
import time

ec2 = boto3.client('ec2', region_name='us-east-1')
route53 = boto3.client('route53', region_name='us-east-1')

def lambda_handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')
    domain = os.environ.get('DOMAIN')
    hosted_zone_id = os.environ.get('HOSTED_ZONE_ID')

    has_ip = False
    while not has_ip:
        try:
            resp = ec2.describe_instances(InstanceIds=[instance_id])
            inst = resp['Reservations'][0]['Instances'][0]
            ip = inst['PublicIpAddress']
            
            has_ip = True
        except:
            time.sleep(1)
            
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
                                'Value': ip
                            }
                        ],
                        'TTL': 300
                    }
                }
            ]
        }
    )
    
