.PHONY: up

up:
	docker compose up -d --wait db
	docker compose build app
	docker compose run --rm app