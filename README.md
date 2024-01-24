This directory is for the RESTful API for the vision-language traffic anomaly detection app.

## Usage

### Environments

- Debian-bookworm
- Python 3.12.1

### Requirements

- Docker-compose

If you haven't installed docker-compose, you could install it by the following script.

```shell
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

### Deploy

You could deploy the server by ruunning the following script.

```shell
docker-compose up --build -d
```

To see the datas in the MongoDB can be seen using mongodb compass. The server url would be

```shell
mongodb://root:laon@localhost:27017
```

The annotation qa tool will be deployed at the following url

```shell
http://localhost:30119
```
