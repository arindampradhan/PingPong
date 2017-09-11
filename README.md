# Pingpong microservice

## Features

* Runs on microservices
* Codebase is deployed to s3 for every version using `zappa update or zappa deploy`
* The flask wsgi uses Amazon http api gateway
* Documentation can be found [here](https://documenter.getpostman.com/view/1206388/pingpong/6taa56p).
* No nginx or ec2 instances required
* Cost on number of requests


## About

* framework - `flask`
* deployment `framework - zappa`
* hosting - `aws lambda`
* documentation - `postman`
* database - `tinydb / tinymongo`
* uses `/tmp` which lambda provides for storing data


## Requirements

* python 3.6
* lambda supports only `python 3.6 and python 2.7`

#### [Go to Documentation](https://documenter.getpostman.com/view/1206388/pingpong/6taa56p)

* https://documenter.getpostman.com/view/1206388/pingpong/6taa56p

#### [hosted](https://9p8dz74000.execute-api.us-east-1.amazonaws.com/dev)

* https://9p8dz74000.execute-api.us-east-1.amazonaws.com/dev

## Start

```
    $ virtaulenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ # or simply go to -> https://9p8dz74000.execute-api.us-east-1.amazonaws.com/dev
    $ python pingpong.py
```