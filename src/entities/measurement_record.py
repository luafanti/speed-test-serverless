import uuid
from datetime import datetime, timezone

class MeasurementInvalidException(Exception):
    pass


class MeasurementRecord:
    def __init__(self, bps = None, kbps = None, mbps = None):

        self.measurement_id = str(uuid.uuid4())
        self.measurement_time = datetime.now(
            timezone.utc).isoformat(' ', 'seconds')

        if any([
            bps is None,
            kbps is None,
            mbps is None
        ]):
            raise MeasurementInvalidException("Missed required attriubtes")
        else:
            self.speed_bps = bps
            self.speed_kbps = kbps
            self.speed_mbps = mbps

    def key(self):
        return {
            'measurementId': self.measurement_id,
            'measurementTime': self.measurement_time
        }

    def to_item(self):
        return {
            **self.key(),
            "speedBps": self.speed_bps,
            "speedKbps": self.speed_kbps,
            "speedMbps": self.speed_mbps,
        }
