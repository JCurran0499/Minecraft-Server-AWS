#!/bin/bash

sudo aws s3 sync /opt/minecraft/server/logs s3://minecraft-world-curran/logs
sudo aws s3 sync /opt/minecraft/server/world s3://minecraft-world-curran/world --delete
