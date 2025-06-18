from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "thermoping"

    # Database settings
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    # MQTT settings
    MOSQUITTO_HOST: str
    MOSQUITTO_PORT: int
    MOSQUITTO_USERNAME: str
    MOSQUITTO_PASSWORD: str

    # InfluxDB settings
    INFLUXDB_HOST: str
    INFLUXDB_PORT: int
    INFLUXDB_ADMIN_TOKEN: str
    INFLUXDB_ORG: str
    INFLUXDB_BUCKET: str
    INFLUXDB_MODE: str
    INFLUXDB_USERNAME: str
    INFLUXDB_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    class Config:
        env_file = ".env"


settings = Settings()
