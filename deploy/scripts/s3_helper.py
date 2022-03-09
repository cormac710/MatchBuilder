import boto3


class S3Helper:
    s3 = boto3.client('s3')

    def __init__(self, bucket_name, region):
        self.bucket = bucket_name
        self.region = region

    def create_bucket(self):
        try:
            self.s3.create_bucket(
                Bucket=self.bucket,
                CreateBucketConfiguration={
                    'LocationConstraint': self.region
                }
            )
        except (self.s3.exceptions.BucketAlreadyExists, self.s3.exceptions.BucketAlreadyOwnedByYou):
            print(f'INFO: Bucket {self.bucket} already exists. Will continue to use.')

    def upload(self, file_to_upload, key):
        print(f'INFO: Uploading file {file_to_upload} to bucket {self.bucket} and key {key}')
        self.s3.upload_file(file_to_upload, self.bucket, key)
