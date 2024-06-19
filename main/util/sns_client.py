import boto3
import os
from domain.constants import SHUTDOWN_MESSAGE

sns_topic = os.environ.get('SNS_TOPIC')

class SNSClient:
    def __init__(self, region):
        self.client = boto3.client("sns", region_name=region)

    def report_shutdown(self):
        return self.client.publish(
            TopicArn=sns_topic, 
            Message=SHUTDOWN_MESSAGE
        )