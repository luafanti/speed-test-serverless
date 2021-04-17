from flask import Flask, render_template, request
from datetime import datetime, timezone
import uuid
import os
import boto3
import json

TABLE_NAME = os.environ['TABLE_NAME']
client = boto3.client('dynamodb')

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/measurement', methods=['POST'])
def save_measurement():

    json_req = request.get_json()
    print(f"Recived measurement record to save {json_req}")

    if is_payload_valid(json_req) is False:
        print(f"Measurement payload is incorrect {json_req}")
        return json.dumps({'success': False, 'msg': 'Measurement payload is incorrect'}), 400, {'ContentType': 'application/json'}

    dynamo_resp = client.put_item(
        TableName=TABLE_NAME,
        Item={
            'measurementId': {'S': str(uuid.uuid4())},
            'measurementTime': {'S': datetime.now(timezone.utc).isoformat(' ', 'seconds')},
            'speedBps': {'N': json_req['speedBps']},
            'speedKbps': {'N': json_req['speedKbps']},
            'speedMbps': {'N': json_req['speedMbps']}
        }
    )
    print(f"Response from DynamoDB = {dynamo_resp}")
    return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}


@app.route('/measurement', methods=['GET'])
def get_measurement():

    dynamo_resp = client.scan(
        TableName=TABLE_NAME
    )

    measurements = []
    for item in dynamo_resp['Items']:
        measurements.append({
            'measurement_time': item['measurementTime']['S'],
            'speed_bps': item['speedBps']['N'],
            'speed_kbps': item['speedKbps']['N'],
            'speed_mbps': item['speedMbps']['N']
        })

    for m in measurements:
        print(f" Item: {m}")

    print(f"Measurements from DynamoDB = {measurements}")
    return render_template('result.html', measurements=measurements)


def is_payload_valid(payload):
    if any([
        payload.get('speedBps') is None,
        payload.get('speedKbps') is None,
        payload.get('speedMbps') is None
    ]):
        return False
    else:
        return True


if __name__ == '__main__':
    app.run()
