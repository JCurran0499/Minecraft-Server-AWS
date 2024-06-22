import os
from util.ec2_client import EC2Client
from util.route53_client import Route53Client
from domain.constants import logger

instance_id = os.environ.get('INSTANCE_ID')
domain = os.environ.get('DOMAIN')
hosted_zone_id = os.environ.get('HOSTED_ZONE_ID')

region = os.environ.get('REGION')
ec2_client = EC2Client(region)
route53_client = Route53Client(region)


@logger.inject_lambda_context
def handler(event, context):
    logger.info(
        "Initiating route53 record update...",
        instance_id=instance_id,
        domain=domain,
        hosted_zone_id=hosted_zone_id
    )

    public_ip = ec2_client.get_public_ip()
    route53_client.update_record(public_ip)

    ec2_client.start_minecraft_server()

    return "success"
