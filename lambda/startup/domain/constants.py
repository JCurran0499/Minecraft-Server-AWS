from aws_lambda_powertools import Logger

logger = Logger()

STARTUP_COMMAND = "sudo java -Xmx1024M -Xms1024M -jar server.jar nogui"