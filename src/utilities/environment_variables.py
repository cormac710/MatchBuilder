from os import environ

IS_DEV = environ.get('IS_DEV', True)

# Dynamo vars
REGION = environ.get('REGION', 'us-east-1')
DYNAMO_HOST = environ.get('DYNAMO_HOST', '127.0.0.1:8000')
DYNAMO_URI = environ.get('DYNAMO_URI', f'http://{DYNAMO_HOST}') if IS_DEV else \
    f'https://dynamodb.{REGION}.amazonaws.com'
WRITE_CAPACITY = environ.get('WRITE_CAPACITY', 1)
READ_CAPACITY = environ.get('READ_CAPACITY', 1)

# flask app vars
ROOT_PORT = environ.get('ROOT_PORT', 5001)
