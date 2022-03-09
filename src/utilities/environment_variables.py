from os import environ

# This should never be set to True in real life but easier for me at the minute (its own AWS costs :) )
IS_DEV = environ.get('IS_DEV', False)

# AWS
REGION = environ.get('AWS_REGION', 'eu-west-1')
AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY', 'dummy')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', 'dummy')

# Dynamo vars
DYNAMO_HOST = environ.get('DYNAMO_HOST', 'localhost:8000')
DYNAMO_URI = environ.get('DYNAMO_URI', f'http://{DYNAMO_HOST}') if IS_DEV else \
    f'https://dynamodb.{REGION}.amazonaws.com'
WRITE_CAPACITY = environ.get('WRITE_CAPACITY', 1)
READ_CAPACITY = environ.get('READ_CAPACITY', 1)

# flask app vars
ROOT_PORT = environ.get('ROOT_PORT', 5001)
