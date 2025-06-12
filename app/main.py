from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings
from app.database import engine
from app.model.user import Base

app = FastAPI(title=settings.PROJECT_NAME)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api")
