import boto3
import os


def get_table():
    dynamodb = boto3.resource("dynamodb", region_name='eu-west-2')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    return table


default_table = get_table()


def save_measurement_record(measurement_record=None, table=default_table):
    try:
        table.put_item(
            Item=measurement_record.to_item()
        )
        return measurement_record
    except Exception as e:
        print("Error creating measurement record")
        print(e)
        error_message = f"Could not create measurement_record {e}"
        return {
            "error": error_message
        }

def get_measurements_record(table=default_table):
    measurements_records = table.scan()
    measurements = []
    for item in measurements_records['Items']:
        measurements.append({
            'measurement_time': item['measurementTime'],
            'speed_bps': item['speedBps'],
            'speed_kbps': item['speedKbps'],
            'speed_mbps': item['speedMbps']
        })
    print(f"Measurements from DynamoDB = {measurements}")
    return measurements
