# Local set up

## Dynamo
### touch /Users/challina/Documents/ProfileApplication/docker/dynamodb
### chmod /Users/challina/Documents/ProfileApplication/docker/dynamodb
docker-compose up -d

## Flask

Python 3.8.9
### Create virtual env
```
virtualenv venv
source venv/bin/activate
pip install -r src/requirements.txt
python -m src.app
```
