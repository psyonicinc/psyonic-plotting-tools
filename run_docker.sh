#!/bin/bash

# Allow Docker to access the X server
xhost +local:docker

cd /home/$USER/psyonic-plotting-tools && docker compose build && docker compose up