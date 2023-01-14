## Installation

Clon repo

```bash
https://github.com/R1ndei/social_network.git
```
go to main project directory

activate virtual environment


```bash
source venv/bin/activate
```

create .env file and fill it

```python
ACCESS_TOKEN_EXPIRE_MINUTES= ...
SECRET_KEY= ...
ALGORITHM= ...
POSTGRES_USER= ...
POSTGRES_PASSWORD= ...
POSTGRES_HOST= ...
POSTGRES_HOST_LOCAL= ...
POSTGRES_PORT= ...
POSTGRES_DB= ...

PGADMIN_DEFAULT_EMAIL= ...
PGADMIN_DEFAULT_PASSWORD= ...

REDIS_PASSWORD= ...
REDIS_URL= ...
REDIS_EXPIRE_SEC= ...

HUNTER_API_KEY= ...

TESTING=0
```
build docker containers

```bash
docker-compose up --build
```

Run tests
```python
docker ps
docker exec "backend_container" pytest
```
env file example
```python
ACCESS_TOKEN_EXPIRE_MINUTES=222
SECRET_KEY=321dsafasdsa32
ALGORITHM=HS256
POSTGRES_USER=test
POSTGRES_PASSWORD=test
POSTGRES_HOST=postgresql_db
POSTGRES_HOST_LOCAL=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=test_db

PGADMIN_DEFAULT_EMAIL=post.test@gmail.com
PGADMIN_DEFAULT_PASSWORD=test

REDIS_PASSWORD=test
REDIS_URL=redis://:test@redis:6379/0
REDIS_EXPIRE_SEC=22

# you can get your own api key here -> emailhunter.co
HUNTER_API_KEY=43434343dsadas

TESTING=0
```
