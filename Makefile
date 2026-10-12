.PHONY: up

up:
	@test -f .env || cp .env.example .env
	docker compose up -d --wait db
	docker compose build app
	docker compose run --rm app