#!/bin/bash
docker build -t=curaengine-build .
docker stop my-curaengine-build
docker rm my-curaengine-build
docker run --name my-curaengine-build -dit curaengine-build
docker exec -it my-curaengine-build bash
