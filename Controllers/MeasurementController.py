from datetime import datetime

from Models.Measurement import Measurement


def get_last_measurement(sensor: str) -> Measurement or None:
    m = Measurement.objects(sensor=sensor).order_by('-timestamp').limit(1).first()
    return m.to_json() if m is not None else None


def new_measurement(data: str) -> Measurement:
    m = Measurement.from_json(data)
    m.timestamp = datetime(m.timestamp[0], m.timestamp[1], m.timestamp[2], m.timestamp[3], m.timestamp[4],
                           m.timestamp[5], 0)
    m.save()
    return m.to_json()
