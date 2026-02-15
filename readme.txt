

docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://192.168.1.152:11434 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main


run out of celex_facts 
uvicorn ui.agno-ui.oi-play:app --host 0.0.0.0 --port 7777 --reload


set

confirm that the celex-facts api server is up
curl http://localhost:7777/v1


go to user icon top right hand side, "admin panel", "setting set in
http://localhost:3000/admin/settings



http://localhost:3000/admin/settings/general

add connection (if pip): 
http://localhost:7777/v1/models
bearer: sk-agent

add connection (if docker): 
http://host.docker.internal:7777/v1
bearer: sk-agent

select coder-agent or finance agent which should forward chart completion to the Ollama model defiend in the oi-play agent
