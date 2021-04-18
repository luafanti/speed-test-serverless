class StubMeasurement:

    def __init__(self):
        pass

    def to_item(self):
        return {
            "measurementId": "random-id-123",
            "measurementTime": "2021-04-18",
            "speedBps": 1000,
            "speedKbps": 100,
            "speedMbps": 10

        }


def mocked_table():
    import boto3
    import os
    dynamodb = boto3.resource("dynamodb", region_name='eu-west-2')
    table = dynamodb.Table(dynamodb.Table(os.environ["TABLE_NAME"]))
    return table


def test_create_measurements(dynamodb_table):
    from src.data.measurement_repository import save_measurement_record
    measurement_instance = StubMeasurement()
    table = mocked_table()
    assert save_measurement_record(
        measurement_record=measurement_instance, table=table) == measurement_instance
