build:
    docker-compose build

stop:
    docker-compose down

logs:
    docker-compose logs -f

dev: build stop && logs
    docker-compose up -d
