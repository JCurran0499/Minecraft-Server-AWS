import boto3
import os
from domain.constants import logger

domain = os.environ.get('DOMAIN')
hosted_zone_id = os.environ.get('HOSTED_ZONE_ID')

class Route53Client:
    def __init__(self, region):
        self.client = boto3.client("route53", region_name=region)

    def update_record(self, public_ip):
        logger.info(f"Updating route53 record {domain} with IP {public_ip}")
        self.client.change_resource_record_sets(
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