"""
Analysis API Endpoints

Clean Architecture: Interface Adapters - Web Controllers
분석 관련 REST API 엔드포인트를 제공합니다.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import structlog

from app.use_cases.analysis.execute_analysis_use_case import (
    ExecuteAnalysisUseCase,
    AnalysisRequest,
    AnalysisResponse,
    PermissionDeniedError,
    InvalidQueryError,
    AnalysisExecutionError
)
from app.schemas.analysis import (
    AnalysisRequestSchema,
    AnalysisResponseSchema,
    ErrorResponseSchema
)
from app.api.dependencies import get_current_user, get_execute_analysis_use_case

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post(
    "/execute",
    response_model=AnalysisResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="분석 실행",
    description="자연어 질문을 받아 데이터 분석을 수행합니다."
)
async def execute_analysis(
    request: AnalysisRequestSchema,
    current_user: Dict[str, Any] = Depends(get_current_user),
    use_case: ExecuteAnalysisUseCase = Depends(get_execute_analysis_use_case)
) -> AnalysisResponseSchema:
    """
    분석 실행 엔드포인트
    
    Clean Architecture: 이 컨트롤러는 HTTP 요청을 Use Case로 변환하는 역할만 담당합니다.
    - HTTP 요청/응답 처리
    - DTO 변환
    - 예외를 HTTP 상태 코드로 매핑
    - Use Case에 위임
    """
    try:
        # HTTP 요청을 Use Case 요청으로 변환
        use_case_request = AnalysisRequest(
            question=request.question,
            user_id=current_user["user_id"],
            connection_id=request.connection_id,
            options=request.options
        )
        
        # Use Case 실행
        logger.info(
            "분석 요청 시작",
            user_id=current_user["user_id"],
            question=request.question[:100] + "..." if len(request.question) > 100 else request.question
        )
        
        result = await use_case.execute(use_case_request)
        
        logger.info(
            "분석 요청 완료",
            query_id=result.query_id,
            status=result.status,
            execution_time_ms=result.execution_time_ms
        )
        
        # Use Case 응답을 HTTP 응답으로 변환
        return AnalysisResponseSchema(
            success=True,
            data={
                "query_id": result.query_id,
                "question": result.question,
                "query_type": result.query_type,
                "status": result.status,
                "result": result.result.to_dict() if result.result else None,
                "execution_time_ms": result.execution_time_ms
            },
            message="분석이 성공적으로 완료되었습니다."
        )
        
    except PermissionDeniedError as e:
        logger.warning(
            "분석 권한 부족",
            user_id=current_user["user_id"],
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        
    except InvalidQueryError as e:
        logger.warning(
            "잘못된 쿼리",
            user_id=current_user["user_id"],
            question=request.question,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except AnalysisExecutionError as e:
        logger.error(
            "분석 실행 오류",
            user_id=current_user["user_id"],
            question=request.question,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="분석 실행 중 오류가 발생했습니다."
        )
        
    except Exception as e:
        logger.error(
            "예상치 못한 오류",
            user_id=current_user["user_id"],
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생했습니다."
        )


@router.post(
    "/execute-with-file",
    response_model=AnalysisResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="파일과 함께 분석 실행",
    description="Excel 파일을 업로드하여 분석을 수행합니다."
)
async def execute_analysis_with_file(
    question: str,
    file: UploadFile = File(...),
    connection_id: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    use_case: ExecuteAnalysisUseCase = Depends(get_execute_analysis_use_case)
) -> AnalysisResponseSchema:
    """
    파일과 함께 분석 실행 엔드포인트
    
    Excel 파일을 업로드하여 분석을 수행합니다.
    """
    try:
        # 파일 검증
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="파일명이 필요합니다."
            )
        
        # 파일 확장자 검증
        allowed_extensions = {'.xlsx', '.xls', '.csv'}
        file_extension = '.' + file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(allowed_extensions)}"
            )
        
        # 파일 크기 검증 (50MB 제한)
        file_data = await file.read()
        max_size = 50 * 1024 * 1024  # 50MB
        
        if len(file_data) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="파일 크기가 너무 큽니다. 최대 50MB까지 지원합니다."
            )
        
        # Use Case 요청 생성
        use_case_request = AnalysisRequest(
            question=question,
            user_id=current_user["user_id"],
            connection_id=connection_id,
            file_data=file_data
        )
        
        # Use Case 실행
        logger.info(
            "파일 분석 요청 시작",
            user_id=current_user["user_id"],
            filename=file.filename,
            file_size=len(file_data),
            question=question[:100] + "..." if len(question) > 100 else question
        )
        
        result = await use_case.execute(use_case_request)
        
        logger.info(
            "파일 분석 요청 완료",
            query_id=result.query_id,
            status=result.status,
            execution_time_ms=result.execution_time_ms
        )
        
        return AnalysisResponseSchema(
            success=True,
            data={
                "query_id": result.query_id,
                "question": result.question,
                "query_type": result.query_type,
                "status": result.status,
                "result": result.result.to_dict() if result.result else None,
                "execution_time_ms": result.execution_time_ms,
                "file_info": {
                    "filename": file.filename,
                    "size": len(file_data)
                }
            },
            message="파일 분석이 성공적으로 완료되었습니다."
        )
        
    except HTTPException:
        # FastAPI HTTPException은 그대로 전파
        raise
        
    except Exception as e:
        logger.error(
            "파일 분석 오류",
            user_id=current_user["user_id"],
            filename=file.filename if file else None,
            error=str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="파일 분석 중 오류가 발생했습니다."
        )


@router.get(
    "/history",
    response_model=Dict[str, Any],
    summary="분석 이력 조회",
    description="사용자의 분석 이력을 조회합니다."
)
async def get_analysis_history(
    limit: int = 10,
    offset: int = 0,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    분석 이력 조회 엔드포인트
    
    TODO: 이 기능은 별도의 Use Case로 구현 예정
    """
    # 임시 구현 - 실제로는 별도 Use Case 필요
    return {
        "success": True,
        "data": {
            "queries": [],
            "total": 0,
            "limit": limit,
            "offset": offset
        },
        "message": "분석 이력을 조회했습니다."
    }


@router.get(
    "/{query_id}",
    response_model=AnalysisResponseSchema,
    summary="분석 결과 조회",
    description="특정 분석 결과를 조회합니다."
)
async def get_analysis_result(
    query_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> AnalysisResponseSchema:
    """
    분석 결과 조회 엔드포인트
    
    TODO: 이 기능은 별도의 Use Case로 구현 예정
    """
    # 임시 구현 - 실제로는 별도 Use Case 필요
    return AnalysisResponseSchema(
        success=True,
        data={
            "query_id": query_id,
            "message": "분석 결과 조회 기능은 구현 예정입니다."
        },
        message="분석 결과를 조회했습니다."
    )
