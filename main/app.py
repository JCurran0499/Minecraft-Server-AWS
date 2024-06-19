import os
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging.correlation_paths import API_GATEWAY_HTTP

from util.ec2_client import EC2Client
from util.lambda_client import LambdaClient
from util.sns_client import SNSClient
from domain.constants import logger, START_MESSAGE, server_expired

domain = os.environ.get('DOMAIN')

api = APIGatewayHttpResolver()

region = "us-east-1"
ec2_client = EC2Client(region)
lambda_client = LambdaClient(region)
sns_client = SNSClient(region)

@api.get("/start")
def start():
    logger.info("START endpoint triggered")

    ec2_client.start_server()
    lambda_client.invoke_dns_function()

    return START_MESSAGE


@api.get("/status")
def status():
    logger.info("STATUS endpoint triggered")

    launch_time, status = ec2_client.get_server_status()

    expire = api.current_event.get_query_string_value("expire", default_value="false")
    if (expire.lower() == "true") and server_expired(launch_time, status):
        logger.info("Server is expired! Shutting down...")
        sns_client.report_shutdown()
        ec2_client.stop_server()

    return status


@api.get("/stop")
def stop():
    logger.info("STOP endpoint triggered")

    ec2_client.stop_server()

    return 'Minecraft server has been stopped'


@logger.inject_lambda_context(correlation_id_path=API_GATEWAY_HTTP)
def handler(event: dict, context: LambdaContext):
    return api.resolve(event, context)
