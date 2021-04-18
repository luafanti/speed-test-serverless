import pytest
import re
from src.entities.measurement_record import MeasurementRecord, MeasurementInvalidException


def test_instantiating_measruements_class_with_no_data_fails():
    with pytest.raises(MeasurementInvalidException):
        MeasurementRecord()


def test_instantiating_measruements_class_with_valid_data():
    bps = 1000
    kbps = 100
    mbps = 10
    measurement_record = MeasurementRecord(bps, kbps, mbps)

    assert measurement_record.speed_bps == bps
    assert measurement_record.speed_kbps == kbps
    assert measurement_record.speed_mbps == mbps
