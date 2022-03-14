import boto3
import time

from botocore.exceptions import ClientError


class CloudFormationHelper:
    client = boto3.client('cloudformation')

    def __init__(self, stack_name, bucket, cf_root_location, main_cf_file_name):
        self.main_stack_name = stack_name
        self.base_cf_location = f'https://{bucket}.s3.eu-west-1.amazonaws.com/{cf_root_location}'
        self.main_template_location = self.base_cf_location + main_cf_file_name

    def get_stack_status(self):
        try:
            data = self.client.describe_stacks(StackName=self.main_stack_name)
        except ClientError:
            # Does does not exist, will create
            print('CLIENT ERROR !!!')
            return False
        return data['Stacks'][0]['StackStatus']

    def upgrade_stack(self):
        return self.client.update_stack(
            StackName=self.main_stack_name,
            TemplateURL=self.main_template_location,
            Parameters=self._generate_stack_parameters(),
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM']
        )

    def _generate_stack_parameters(self):
        return [
            {
                'ParameterKey': 'TemplateRootUrl',
                'ParameterValue': self.base_cf_location
            }
        ]

    def create_stack(self):
        print(f'INFO: creating main strac from template: {self.main_template_location}')
        return self.client.create_stack(
            StackName=self.main_stack_name,
            TemplateURL=self.main_template_location,
            Parameters=self._generate_stack_parameters(),
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM']
        )

    def describe_stack(self, stack_name=None):
        if not stack_name:
            stack_name = self.main_stack_name
        return self.client.describe_stacks(StackName=stack_name)

    def stack_status(self, stack_name=None):
        stack_details = self.describe_stack(stack_name)
        return stack_details['Stacks'][0]['StackStatus']

    def wait_for_stack_upgrade_create_status(self, status_to_wait_for, stack_name=None, time_to_sleep=5):
        stack_status = self.stack_status(stack_name)
        while stack_status != status_to_wait_for:
            if stack_status in ['ROLLBACK_IN_PROGRESS', 'ROLLBACK_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']:
                print(f'ERROR: stack entered status {stack_status}, this is incorrect please investigate!!!')
                return False
            print(f'INFO: stack in status {stack_status}, waiting another {time_to_sleep}s')
            time.sleep(time_to_sleep)
            stack_status = self.stack_status(stack_name)
        print(f'INFO: stack successfully entered {stack_status}')
        return True
