import boto3
import os

from domain.constants import logger

dns_function = os.environ.get('DNS_FUNCTION')

class LambdaClient:
    def __init__(self, region):
        self.client = boto3.client("lambda", region_name=region)

    def invoke_dns_function(self):
        logger.info("Invoking DNS update function...")
        return self.client.invoke(
            FunctionName=dns_function,
            InvocationType='Event'
        )