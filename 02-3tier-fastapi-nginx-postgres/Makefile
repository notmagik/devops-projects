up:
	docker compose up -d --build

down:
	docker compose down

ps:
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

logs:
	docker compose logs -f --tail=200

curl-health:
	curl -sS http://localhost:8080/health && echo

curl-db:
	curl -sS http://localhost:8080/db && echo
