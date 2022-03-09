"""
Main script for stack creation/uograde and deploying services to AWS.
"""
import glob
import pathlib
import os
import sys

from deploy.scripts.cloud_formation_helper import CloudFormationHelper
from scripts.s3_helper import S3Helper

# constants should be ENV variables OR parameter store etc...
REGION = 'eu-west-1'
CF_BUCKET_NAME = 'cf-templates-match-builder-' + REGION
CF_LOCAL_FOLDER_NAME = '/cf/*'
S3_KEY_ROOT = 'match-builder/cf'
MAIN_CF_FILE_NAME = '/main.yaml'
# This will definitely need to be a parameter - will be test stacks i.e. based off branch name (not main)
MAIN_STACK_NAME = 'MatchBuilder'


def create_templates_bucket_and_upload_templates():
    s3 = S3Helper(CF_BUCKET_NAME, REGION)
    s3.create_bucket()
    template_location = str(pathlib.Path(__file__).parent.resolve()) + CF_LOCAL_FOLDER_NAME
    for file in glob.glob(template_location):
        key = S3_KEY_ROOT + os.path.basename(file)
        s3.upload(file, key)


def create_update_stack():
    cf = CloudFormationHelper(MAIN_STACK_NAME, CF_BUCKET_NAME, S3_KEY_ROOT, MAIN_CF_FILE_NAME)
    complete_stack_statuses = ['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']
    main_stack_status = cf.get_stack_status()
    if not main_stack_status:
        print(f'INFO: Creating stack: {MAIN_STACK_NAME}')
        stack_create_response = cf.create_stack()
        check_stack_status_code(stack_create_response)
        stack_status = cf.wait_for_stack_upgrade_create_status('CREATE_COMPLETE')
        if not stack_status:
            sys.exit(1)
    elif main_stack_status in complete_stack_statuses:
        print('Upgrade...')
        stack_updated_response = cf.upgrade_stack()
        check_stack_status_code(stack_updated_response)
        stack_status = cf.wait_for_stack_upgrade_create_status('UPDATE_COMPLETE')
        if not stack_status:
            sys.exit(1)
    else:
        print(f'ERROR: Stack in state {main_stack_status}, create/upgrade can not complete')
        sys.exit(1)


def check_stack_status_code(stack_create_response):
    response_code = stack_create_response['ResponseMetadata']['HTTPStatusCode']
    print(f'response_code {response_code}')
    if response_code != 200:
        print(f'ERROR: Issue creating stack, returned and error code of {response_code}')
        sys.exit(1)


create_templates_bucket_and_upload_templates()
create_update_stack()
