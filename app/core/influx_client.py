from influxdb_client import InfluxDBClient
from app.core.config import settings


def create_influx_client():
    client = InfluxDBClient(
        url=f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}",
        token=settings.INFLUXDB_ADMIN_TOKEN,
        org=settings.INFLUXDB_ORG,
    )
    return client
