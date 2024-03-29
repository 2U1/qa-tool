# QA Tool

This repository is for machine learning dataset quality assurance application.<br>

**It only supports Vision-Language dataset in current version.**

## Examples

View of data list. Check shows if you have inspected the data. You can move to the inspectation view by clicking the link in the detail.

![demo1](img/demo1.png)

By clicking the button accept and reject, you can send the result to the database. The button is hilighted unless you change the quality status.

![demo2](img/demo2.png)

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

### Dataset Preparation

#### Images

You should place your images into `/data/vlm/images`

#### Text

You can upload the data from local(File size should be under 1GB).<br>
The format of [LLaVA](https://huggingface.co/datasets/liuhaotian/LLaVA-Instruct-150K?row=0) is only supported for now.

### Deploy

You could deploy the server by ruunning the following script.

```shell
docker-compose up --build -d
```

The annotation qa tool will be deployed at the following url if you are going to use it in local.

```shell
http://localhost:30010
```

### Data Upload

You can upload the data by using the upload feature in the navigation bar.

### Export Data

You can download the data by using the export feature in the navigation bar. The downloaded data will be saved in `/data/{datasetname}/exported`.

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

- Admin user
- User Profile
- Supporting other dataset types
- Adding Annotation Feature
