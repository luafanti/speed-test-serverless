from flask import Flask, render_template, request
from datetime import datetime, timezone
import speedtest
import os
import boto3
import json

TABLE_NAME = os.environ['TABLE_NAME']
client = boto3.client('dynamodb')

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        speed_test = speedtest.Speedtest()
        speed_test.get_servers()
        speed_test.get_best_server()
        speed_test.download()
        speed_test.upload()
        speed_test_result = speed_test.results.dict()

        download = round(speed_test_result["download"]/1000, 2)
        upload = round(speed_test_result["upload"]/1000, 2)
        ping = round(speed_test_result["ping"])
        provider = speed_test_result["client"]["isp"]

        return render_template('index.html', download=download, upload=upload, ping=ping, provider=provider)
    else:
        return render_template('index.html', download=0, upload=0, ping=0, provider="...")


@app.route('/measurement', methods=['POST'])
def save_measurement():

    json_req = request.get_json()
    print(f"Recived measurment to save {json_req}")

    if is_payload_valid(json_req) is False:
        return json.dumps({'success': False, 'msg': 'Measurment payload is incorrect'}), 400, {'ContentType': 'application/json'}

    dynamo_resp = client.put_item(
        TableName=TABLE_NAME,
        Item={
            'provider': {'S': json_req['provider']},
            'measurementTime': {'S': datetime.now(timezone.utc).isoformat(' ', 'seconds')},
            'ping': {'S': json_req['ping']},
            'download': {'S': json_req['download']},
            'upload': {'S': json_req['download']}
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
            'provider': item['provider']['S'],
            'ping': item['ping']['S'],
            'download': item['download']['S'],
            'upload': item['upload']['S']
        })

    for m in measurements:
        print(f" Item: {m}")

    print(f"Measurements from DynamoDB = {measurements}")
    return render_template('result.html', measurements=measurements)


def is_payload_valid(payload):
    if any([
        payload.get('provider') is None,
        payload.get('ping') is None,
        payload.get('download') is None,
        payload.get('upload') is None
    ]):
        return False
    else:
        return True


if __name__ == '__main__':
    app.run()
