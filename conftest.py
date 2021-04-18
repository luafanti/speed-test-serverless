import os

import boto3
import pytest

from moto import mock_dynamodb2

os.environ['TABLE_NAME'] = 'measurements'
os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def dynamodb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.resource('dynamodb', region_name='eu-west-2')


@pytest.fixture(scope='function')
def dynamodb_table(dynamodb):
    table = dynamodb.create_table(
        TableName='measurements',
        KeySchema=[
            {
                'AttributeName': 'measurementId',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'measurementTime',
                'KeyType': 'RANG'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'measurementId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'measurementTime',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='measurements')
    yield
