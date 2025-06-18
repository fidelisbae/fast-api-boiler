from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router
from app.database import engine
from app.model.user import Base
from app.service.sensor_service import start_mqtt_subscriber

app = FastAPI(title=settings.PROJECT_NAME)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    # MQTT 구독자 시작
    clients = start_mqtt_subscriber()
    app.state.mqtt_clients = clients


@app.on_event("shutdown")
async def shutdown_event():
    # MQTT 구독자 종료
    if hasattr(app.state, "mqtt_clients"):
        for client in app.state.mqtt_clients:
            client.loop_stop()
            client.disconnect()
