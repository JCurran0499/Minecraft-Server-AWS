import boto3

ssm_client = boto3.client("ssm", region_name="us-east-1")

resp = ssm_client.send_command(
    InstanceIds=["i-056f277954bc92269"],
    DocumentName="AWS-RunShellScript",
    Parameters={'commands': ["cd /opt/minecraft/server", "sudo java -Xmx1024M -Xms1024M -jar server.jar nogui"]}
)
print(resp)