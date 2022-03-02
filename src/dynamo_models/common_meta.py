from src.utilities.environment_variables import REGION, HOST, WRITE_CAPACITY, READ_CAPACITY

class CommonMeta:
    region = REGION
    host = HOST
    write_capacity_units = WRITE_CAPACITY
    read_capacity_units = READ_CAPACITY
    aws_access_key_id = "dummy"
    aws_secret_access_key = "dummy"
