from flask import Flask, render_template, request
from src.entities.measurement_record import MeasurementRecord
from src.data.measurement_repository import save_measurement_record, get_measurements_record

import os
import json

TABLE_NAME = os.environ['TABLE_NAME']

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/measurement', methods=['POST'])
def save_measurement():
    json_req = request.get_json()
    print(f"Recived measurement record to save {json_req}")
    measurement_record = MeasurementRecord(
        json_req['speedBps'], json_req['speedKbps'], json_req['speedMbps'])
    save_measurement_record(measurement_record)
    return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}


@app.route('/measurement', methods=['GET'])
def get_measurement():
    measurements = get_measurements_record()
    return render_template('result.html', measurements=measurements)


if __name__ == '__main__':
    app.run()
