from os import environ

# Dynamo vars
REGION = environ.get('REGION', 'us-east-1')
# https://dynamodb.{GPR_AWS_REGION}.amazonaws.com
HOST = environ.get('HOST', 'http://127.0.0.1:8000')
WRITE_CAPACITY = environ.get('WRITE_CAPACITY', 1)
READ_CAPACITY = environ.get('READ_CAPACITY', 1)

# flask app vars
ROOT_PORT = environ.get('ROOT_PORT', 5000)
