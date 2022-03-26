from src.utilities.environment_variables import REGION, DYNAMO_URI, WRITE_CAPACITY, READ_CAPACITY, AWS_ACCESS_KEY, \
    AWS_SECRET_ACCESS_KEY


class CommonMeta:
    region = REGION
    host = DYNAMO_URI
    write_capacity_units = WRITE_CAPACITY
    read_capacity_units = READ_CAPACITY
    if AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY:
        aws_access_key_id = AWS_ACCESS_KEY
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
