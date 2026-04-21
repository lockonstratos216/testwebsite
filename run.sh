#!/bin/bash

echo "Starting Dockerized web application...."
echo "This might take a while...."

docker-compose down
docker-compose up --build -d
docker-compose logs -f

echo "Running at http://localhost:5000"
echo "To stop it run stop.sh on tis terminal"