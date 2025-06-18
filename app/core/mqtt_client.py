import paho.mqtt.client as mqtt
from app.core.config import settings


def create_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(settings.MOSQUITTO_USERNAME, settings.MOSQUITTO_PASSWORD)
    client.connect(settings.MOSQUITTO_HOST, settings.MOSQUITTO_PORT)
    return client
