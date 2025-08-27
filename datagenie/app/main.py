"""
DataGenie FastAPI Application Entry Point

Clean Architecture: Main Composition Root
애플리케이션의 진입점이며 모든 의존성을 연결합니다.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import structlog

from app.config.settings import get_settings
from app.config.logging import setup_logging
from app.api.v1.analysis import router as analysis_router
from app.infrastructure.di_container import get_di_container

# 로깅 설정
setup_logging()
logger = structlog.get_logger(__name__)

# 설정 로드
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 생명주기 관리
    
    Clean Architecture: 시스템 초기화 및 정리를 담당
    """
    # 시작시 초기화
    logger.info("DataGenie 애플리케이션 시작", version=settings.app_version)
    
    try:
        # DI 컨테이너 초기화
        container = get_di_container()
        logger.info("의존성 주입 컨테이너 초기화 완료")
        
        # 추가 초기화 작업들
        # TODO: 데이터베이스 연결, 캐시 초기화 등
        
        yield
        
    except Exception as e:
        logger.error("애플리케이션 초기화 실패", error=str(e))
        raise
    finally:
        # 종료시 정리
        logger.info("DataGenie 애플리케이션 종료")
        # TODO: 리소스 정리


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="DataGenie",
    description="LLM-based Data Query, Analysis & Visualization Service",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)

# API 라우터 등록
app.include_router(
    analysis_router,
    prefix="/api/v1",
    tags=["analysis"]
)


# 기본 엔드포인트들
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to DataGenie! 🧞‍♂️",
        "description": "LLM-based Data Query, Analysis & Visualization Service",
        "version": settings.app_version,
        "docs": "/docs",
        "status": "running",
        "features": {
            "nlp_processing": "implemented",
            "database_query": "implemented", 
            "excel_analysis": "implemented",
            "visualization": "implemented"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and monitoring"""
    try:
        # TODO: 실제 헬스체크 로직 구현
        # - 데이터베이스 연결 확인
        # - Redis 연결 확인
        # - 외부 서비스 상태 확인
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "DataGenie",
            "version": settings.app_version,
            "environment": "development" if settings.debug else "production"
        }
    except Exception as e:
        logger.error("헬스체크 실패", error=str(e))
        raise HTTPException(status_code=503, detail="Service Unavailable")


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "api_version": "v1",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "features": {
            "analysis_execution": "available",
            "file_upload": "available",
            "query_history": "planned",
            "user_management": "planned"
        },
        "limits": {
            "max_file_size_mb": settings.max_file_size_mb,
            "max_query_rows": 10000,
            "rate_limit_per_minute": settings.rate_limit_per_minute
        }
    }


# 전역 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리"""
    logger.error(
        "처리되지 않은 예외",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "서버 내부 오류가 발생했습니다.",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )


if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
