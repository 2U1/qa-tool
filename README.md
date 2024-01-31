# QA Tool

This directory is for the RESTful API for the data annoation QA app.<br>

**It only supports Vision-Language dataset in current version.**

## Examples

View of data list. Check shows if you have inspected the data. You can move to the inspectation view by clicking the link in the detail.

![demo1](img/demo1.PNG)

By clicking the button accept and reject, you can send the result to the database. The button is hilighted unless you change the quality status.

![demo2](img/deom2.PNG)

## Usage

### Environments

- Debian-bookworm
- Python 3.12.1

### Requirements

#### Docker-compose

If you haven't installed docker-compose, you could install it by the following script.

```shell
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

#### Images

You should place your images into `/frontend/public/images`

### Deploy

You could deploy the server by ruunning the following script.

```shell
docker-compose up --build -d
```

The annotation qa tool will be deployed at the following url

```shell
http://localhost:30119
```

### Database

To see the datas in the MongoDB can be seen using mongodb compass (Because express isn't running). The server url would be

```shell
mongodb://root:1234@localhost:27017
```

Note that this is the initial id and password. You could change the `name` and `password` in [docker-compose file](docker-compose.yml). After chaning the `name` and the `password` of mongodb you should change the DB_URL in the [env file](api/.env)
<br><br>
You can use mongosh by

```shell
docker exec -it qadb mongosh
```

### Security

For secure datas you need change the `SECRET_KEY` in the [env file](api/.env). Also the `name` and `password` of the mongodb

### Serving as server

You need to change the ip address in [nginx setting file](./qa) and [frontend env file](frontend/.env.production)

## Future update

- User Profile
- Supporting other dataset types
- Create external api for sending image
