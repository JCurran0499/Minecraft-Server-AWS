#!/bin/bash

sudo aws s3 sync /opt/minecraft/server/world s3://minecraft-world-curran/world --delete
