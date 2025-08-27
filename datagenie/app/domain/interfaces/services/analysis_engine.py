"""
Analysis Engine Interface

Clean Architecture: 도메인에서 정의하는 분석 엔진 인터페이스
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.domain.value_objects.analysis_result import AnalysisResult


class IAnalysisEngine(ABC):
    """
    분석 엔진 인터페이스
    
    Clean Architecture: 도메인에서 정의하는 분석 엔진의 계약
    """
    
    @abstractmethod
    async def execute_analysis(
        self,
        question: str,
        connection_id: Optional[str] = None,
        file_data: Optional[bytes] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> AnalysisResult:
        """
        분석 실행
        
        Args:
            question: 사용자 질문
            connection_id: 데이터베이스 연결 ID (선택사항)
            file_data: 파일 데이터 (선택사항)
            options: 추가 옵션
            
        Returns:
            분석 결과
        """
        pass
    
    @abstractmethod
    async def analyze_question(self, question: str) -> Dict[str, Any]:
        """
        질문 분석
        
        Args:
            question: 사용자 질문
            
        Returns:
            분석된 질문 정보
        """
        pass
