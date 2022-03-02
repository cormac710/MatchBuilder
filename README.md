# Local set up

## Run all in docker
```
# Create directory to mount dynamo 
mkdir docker
docker-compose up -d
```

### Add a Person
Send a POST request to: http://127.0.0.1:5001/api/person/

You can use the following body (at least until swagger is up and running)
```
{
    "email": "cormac@email.com",
    "first_name": "cormac",
    "age": 22
}
```

Note: ive set it up using 5001 for local dev reasons on my own machine instead of the default 5000

## Run as application 

### Dynamo (still using dynamo docker container)
Comment out the "backend" configuration in docker-compose.yaml
```
# Create directory to mount dynamo 
mkdir docker
docker-compose up -d
```

### Flask

Python 3.8.9
#### Create virtual env
```
virtualenv venv
source venv/bin/activate
pip install -r src/requirements.txt
python -m src.app
```
