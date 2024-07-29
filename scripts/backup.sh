#!/bin/bash

read -p "Is the server shut down? (Y/N): " SHUTDOWN
if [ "$SHUTDOWN" = "Y" ]; then
    sudo aws s3 sync /opt/minecraft/server/world s3://minecraft-world-curran/world --delete
fi
