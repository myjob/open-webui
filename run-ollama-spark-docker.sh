#!/bin/bash

host_port=11434
container_port=11434


docker_args="-d -v ollama:/root/.ollama -p $host_port:$container_port --name ollama ollama/ollama"


docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://192.168.1.152:11434 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

docker image prune -f
