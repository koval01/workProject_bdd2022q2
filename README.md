# WorkProject

Hello, let's start by deploying the project in Docker.

If you are using Ubuntu then follow these steps:

```shell
apt install -y docker.io docker-compose
```

After installing docker there composer, you need to download the repository to the machine

```shell
git clone https://github.com/koval01/workProject_bdd2022q2
```

Next, we will assemble and launch the project
```shell
docker-compose build && docker-compose up -d
```
(The _-d_ flag puts all tasks in the background)

### Follow these steps to create a super user.

Find out the ID of the container
```shell
docker ps
```
(You need a container - workproject_bdd2022q2_app)

Next, connect to his terminal
```shell
docker exec -t -i CONTAINER_ID bash
```

In it, call the manager and create a super user
```shell
python manage.py createsuperuser
```

## Basic use this application

Replace localhost:8000 to your address. And set https schema if you are use this

```shell
curl -X POST "http://localhost:8000/register/" -H "Content-Type: application/json" -d "{\"username\": \"user\", \"password\": \"password_user\", \"password2\": \"password_user\", \"email\": \"mail@example.com\"}"
```

Generate auth token 
```shell
curl -X POST "http://localhost:8000/api-token-auth/" -H "Content-Type: application/json" -d "{\"username\": \"user\", \"password\": \"password_user\"}"
```

For view your images. (Replace ORDERED_TOKEN to your token)
```shell
curl -X GET "http://localhost:8000/images/" -H "Authorization: Token ORDERED_TOKEN"
```