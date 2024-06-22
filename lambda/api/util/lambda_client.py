import boto3
import os
from domain.constants import logger

startup_function = os.environ.get('STARTUP_FUNCTION')

class LambdaClient:
    def __init__(self, region):
        self.client = boto3.client("lambda", region_name=region)

    def invoke_startup_function(self):
        logger.info("Invoking server startup function...")
        return self.client.invoke(
            FunctionName=startup_function,
            InvocationType='Event'
        )
    