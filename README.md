# Local set up

## Dynamo
```
# Create directory to mount dynamo 
mkdir docker
docker-compose up -d
```

## Flask

Python 3.8.9
### Create virtual env
```
virtualenv venv
source venv/bin/activate
pip install -r src/requirements.txt
python -m src.app
```
