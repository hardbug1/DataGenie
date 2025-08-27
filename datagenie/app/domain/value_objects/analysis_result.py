"""
Analysis Result Value Object

Clean Architecture: 분석 결과를 나타내는 값 객체
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass(frozen=True)
class AnalysisResult:
    """
    분석 결과 값 객체
    
    Clean Architecture: 불변 값 객체로 분석 결과를 캡슐화
    """
    
    # 기본 정보
    analysis_type: str  # "database", "excel", "general"
    question: str
    
    # 실행 정보
    sql_query: Optional[str] = None
    generated_code: Optional[str] = None
    execution_success: bool = True
    
    # 결과 데이터
    data: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    row_count: Optional[int] = None
    
    # 시각화 정보
    chart_type: Optional[str] = None
    chart_config: Optional[Dict[str, Any]] = None
    chart_data: Optional[str] = None  # JSON 형태의 차트 데이터
    
    # 인사이트 및 요약
    summary: Optional[str] = None
    insights: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    
    # 메타데이터
    metadata: Optional[Dict[str, Any]] = None
    
    def has_data(self) -> bool:
        """결과에 데이터가 있는지 확인"""
        return self.data is not None and len(self.data) > 0
    
    def has_visualization(self) -> bool:
        """시각화가 생성되었는지 확인"""
        return self.chart_type is not None and self.chart_data is not None
    
    def has_insights(self) -> bool:
        """인사이트가 생성되었는지 확인"""
        return self.insights is not None and len(self.insights) > 0
    
    def get_data_preview(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        데이터 미리보기 반환
        
        Args:
            limit: 반환할 최대 행 수
            
        Returns:
            제한된 데이터 목록
        """
        if not self.has_data():
            return []
        
        return self.data[:limit]
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "analysis_type": self.analysis_type,
            "question": self.question,
            "sql_query": self.sql_query,
            "generated_code": self.generated_code,
            "execution_success": self.execution_success,
            "data": self.data,
            "columns": self.columns,
            "row_count": self.row_count,
            "chart_type": self.chart_type,
            "chart_config": self.chart_config,
            "chart_data": self.chart_data,
            "summary": self.summary,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "metadata": self.metadata
        }
