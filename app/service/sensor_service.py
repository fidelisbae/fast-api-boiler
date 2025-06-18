import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading

from influxdb_client import Point
from app.core.config import settings
from app.core.mqtt_client import create_mqtt_client
from app.core.influx_client import create_influx_client


class SensorDataProcessor:
    def __init__(self, num_workers=5):
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.data_queue = Queue()
        self.write_api = create_influx_client().write_api()
        self.start_workers(num_workers)

    def start_workers(self, num_workers):
        for _ in range(num_workers):
            worker = threading.Thread(target=self.worker_loop, daemon=True)
            worker.start()
            print(f"Started worker thread {worker.name}")

    def worker_loop(self):
        while True:
            try:
                msg = self.data_queue.get()
                self.process_message(msg)
            except Exception as e:
                print(f"Worker error: {e}")
            finally:
                self.data_queue.task_done()

    def process_message(self, msg):
        try:
            data = json.loads(msg.payload.decode())
            sensor_data = data["sensor"]

            # 온도와 습도 데이터 추출
            temperature = None
            humidity = None

            for sensor in sensor_data:
                if sensor["2"] == "T":
                    temperature = sensor["3"]
                elif sensor["2"] == "HUM":
                    humidity = sensor["3"]

            if temperature is not None and humidity is not None:
                print(f"온도: {temperature:.2f}°C, 습도: {humidity:.2f}%")

                # InfluxDB에 데이터 저장
                did = data.get("DID", "unknown")
                point = (
                    Point(did)
                    .field("temperature", temperature)
                    .field("humidity", humidity)
                    .time(datetime.utcnow())
                )

            self.write_api.write(settings.INFLUXDB_BUCKET, settings.INFLUXDB_ORG, point)
            print(f"Data saved to InfluxDB: {data}")
        except Exception as e:
            print(f"Error processing message: {e}")
            # 실패한 메시지를 큐에 다시 넣지 않고 로그만 남깁니다.


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"MQTT: Connected to broker")
        client.subscribe("/device/sensor")
        print(f"MQTT: Subscribed to /device/sensor")
    else:
        print(f"MQTT: Connection failed with code {rc}")


def on_message(client, userdata, msg):
    print(f"MQTT: Received message on topic {msg.topic}")
    userdata["processor"].data_queue.put(msg)


def start_mqtt_subscriber():
    processor = SensorDataProcessor(num_workers=5)  # 5개의 워커 스레드
    client = create_mqtt_client()
    client._client_id = "mqtt_client"
    client.user_data_set({"processor": processor})
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"MQTT: Connecting to {settings.MOSQUITTO_HOST}:{settings.MOSQUITTO_PORT}")
    client.connect(settings.MOSQUITTO_HOST, settings.MOSQUITTO_PORT)
    client.loop_start()
    print("MQTT: Client started")

    return [client]


def stop_mqtt_subscribers(clients):
    for client in clients:
        client.loop_stop()
        client.disconnect()
