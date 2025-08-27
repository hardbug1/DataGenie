"""
Frontend Services for DataGenie

백엔드 API와의 통신을 담당하는 서비스 모듈입니다.
Clean Architecture: Interface Layer Services
"""

import requests
import json
import os
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import asyncio
import aiohttp


class DataGenieAPIService:
    """DataGenie 백엔드 API와 통신하는 서비스"""
    
    def __init__(self, base_url: str = None):
        """API 서비스 초기화"""
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.session = None
        
    async def create_session(self):
        """HTTP 세션 생성"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        """HTTP 세션 종료"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def health_check(self) -> bool:
        """백엔드 서버 상태 확인"""
        try:
            await self.create_session()
            async with self.session.get(f"{self.base_url}/health") as response:
                return response.status == 200
        except Exception:
            return False
    
    async def execute_analysis(
        self,
        question: str,
        data_source_type: str = "database",
        connection_id: Optional[str] = None,
        file_data: Optional[bytes] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """자연어 분석 요청 실행"""
        
        try:
            await self.create_session()
            
            payload = {
                "question": question,
                "query_type": "natural_language",
                "connection_id": connection_id or "default",
                "auto_visualize": options.get("auto_visualize", True),
                "include_insights": options.get("include_insights", True),
                "preferred_chart_type": options.get("chart_type", "auto")
            }
            
            headers = {"Content-Type": "application/json"}
            
            async with self.session.post(
                f"{self.base_url}/api/v1/analysis/execute",
                json=payload,
                headers=headers
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "data": result
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"API Error {response.status}: {error_text}"
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection Error: {str(e)}"
            }
    
    def sync_execute_analysis(self, *args, **kwargs) -> Dict[str, Any]:
        """동기 버전의 분석 실행 (Gradio용)"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.execute_analysis(*args, **kwargs))


class DemoDataService:
    """데모용 데이터 생성 서비스"""
    
    @staticmethod
    def extract_time_period(question: str) -> str:
        """사용자 질문에서 기간을 추출하여 SQL INTERVAL 형식으로 변환"""
        import re
        
        # 한글 기간 표현 매핑
        period_map = {
            r'1개월|한달|한 달': '1 month',
            r'2개월|두달|두 달|2달': '2 months', 
            r'3개월|세달|세 달|3달': '3 months',
            r'4개월|네달|네 달|4달': '4 months',
            r'5개월|다섯달|다섯 달|5달': '5 months',
            r'6개월|여섯달|여섯 달|6달|반년': '6 months',
            r'1년|일년|12개월': '1 year',
            r'2년|이년|24개월': '2 years',
            r'최근': '3 months',  # 기본값
        }
        
        question_lower = question.lower()
        
        # 패턴 매칭으로 기간 추출
        for pattern, interval in period_map.items():
            if re.search(pattern, question_lower):
                return interval
        
        # 숫자 + 개월/달 패턴 (예: "5개월", "12달")
        number_pattern = r'(\d+)(?:개월|달)'
        match = re.search(number_pattern, question_lower)
        if match:
            num = int(match.group(1))
            return f"{num} month{'s' if num > 1 else ''}"
        
        # 기본값: 3개월
        return '3 months'
    
    @staticmethod
    def generate_sales_data(question: str) -> Tuple[pd.DataFrame, str]:
        """매출 관련 데모 데이터 생성"""
        import random
        
        if "월별" in question or "매출" in question:
            # 🔥 동적 기간 추출 적용!
            time_period = DemoDataService.extract_time_period(question)
            
            months = ['1월', '2월', '3월', '4월', '5월', '6월']
            sales = [random.randint(1000, 5000) for _ in months]
            growth = [f"{random.randint(-10, 30)}%" for _ in months]
            
            data = pd.DataFrame({
                '월': months,
                '매출액(만원)': sales,
                '전년동월대비': growth,
                '주문수': [random.randint(50, 200) for _ in months]
            })
            
            sql = f"""
SELECT 
    DATE_TRUNC('month', order_date) as 월,
    SUM(total_amount) / 10000 as 매출액_만원,
    COUNT(*) as 주문수,
    ROUND(
        (SUM(total_amount) - LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date))) 
        / LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) * 100, 2
    ) as 전년동월대비
FROM orders 
WHERE order_date >= CURRENT_DATE - INTERVAL '{time_period}'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY 월;
            """
            
        elif "제품" in question or "상품" in question:
            # 🔥 동적 기간 추출 적용!
            time_period = DemoDataService.extract_time_period(question)
            
            products = ['스마트폰', '노트북', '태블릿', '헤드폰', '스마트워치']
            sales = [random.randint(500, 3000) for _ in products]
            
            data = pd.DataFrame({
                '제품명': products,
                '매출액(만원)': sales,
                '판매량': [random.randint(10, 100) for _ in products],
                '매출기여도(%)': [round(s/sum(sales)*100, 1) for s in sales]
            })
            
            sql = f"""
SELECT 
    p.product_name as 제품명,
    SUM(oi.quantity * oi.unit_price) / 10000 as 매출액_만원,
    SUM(oi.quantity) as 판매량,
    ROUND(SUM(oi.quantity * oi.unit_price) / (SELECT SUM(quantity * unit_price) FROM order_items) * 100, 1) as 매출기여도
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
WHERE o.order_date >= CURRENT_DATE - INTERVAL '{time_period}'
GROUP BY p.product_name
ORDER BY 매출액_만원 DESC;
            """
            
        else:
            # 기본 데이터
            categories = ['온라인', '오프라인', '모바일', '전화주문']
            values = [random.randint(500, 2000) for _ in categories]
            
            data = pd.DataFrame({
                '채널': categories,
                '매출액(만원)': values,
                '비중(%)': [round(v/sum(values)*100, 1) for v in values]
            })
            
            sql = """
SELECT 
    channel as 채널,
    SUM(total_amount) / 10000 as 매출액_만원,
    ROUND(SUM(total_amount) / (SELECT SUM(total_amount) FROM orders) * 100, 1) as 비중
FROM orders 
GROUP BY channel
ORDER BY 매출액_만원 DESC;
            """
        
        return data, sql.strip()
    
    @staticmethod
    def generate_chart(data: pd.DataFrame, chart_type: str = "auto") -> go.Figure:
        """데이터에 따른 차트 생성"""
        
        if data.empty:
            return go.Figure()
        
        # 첫 번째와 두 번째 컬럼을 기본으로 사용
        x_col = data.columns[0]
        y_col = data.columns[1] if len(data.columns) > 1 else data.columns[0]
        
        # 자동 차트 타입 결정
        if chart_type == "auto" or chart_type == "자동 선택":
            if "월" in x_col or "일" in x_col:
                chart_type = "선 차트"
            elif len(data) <= 10 and data[y_col].dtype in ['int64', 'float64']:
                chart_type = "막대 차트"
            else:
                chart_type = "막대 차트"
        
        # 차트 생성
        if chart_type in ["막대 차트", "bar"]:
            fig = px.bar(
                data,
                x=x_col,
                y=y_col,
                title=f"{x_col}별 {y_col}",
                color=y_col,
                color_continuous_scale='blues'
            )
        elif chart_type in ["선 차트", "line"]:
            fig = px.line(
                data,
                x=x_col,
                y=y_col,
                title=f"{x_col}별 {y_col} 추이",
                markers=True
            )
        elif chart_type in ["파이 차트", "pie"]:
            fig = px.pie(
                data,
                names=x_col,
                values=y_col,
                title=f"{x_col}별 {y_col} 비중"
            )
        else:
            # 기본값: 막대 차트
            fig = px.bar(
                data,
                x=x_col,
                y=y_col,
                title=f"{x_col}별 {y_col}",
                color=y_col,
                color_continuous_scale='viridis'
            )
        
        # 차트 스타일 설정
        fig.update_layout(
            title_font_size=20,
            title_x=0.5,
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True if chart_type in ["파이 차트", "pie"] else False
        )
        
        return fig
    
    @staticmethod
    def generate_insights(question: str, data: pd.DataFrame) -> str:
        """데이터 기반 인사이트 생성"""
        
        if data.empty:
            return "데이터가 없어 인사이트를 생성할 수 없습니다."
        
        # 기본 통계
        numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) == 0:
            return "수치 데이터가 없어 인사이트를 생성할 수 없습니다."
        
        main_col = numeric_cols[0]
        total = data[main_col].sum()
        avg = data[main_col].mean()
        max_idx = data[main_col].idxmax()
        min_idx = data[main_col].idxmin()
        max_val = data.loc[max_idx, main_col]
        min_val = data.loc[min_idx, main_col]
        max_category = data.loc[max_idx, data.columns[0]]
        min_category = data.loc[min_idx, data.columns[0]]
        
        insights = f"""
## 📊 분석 결과 요약

**질문**: {question}

### 🔍 주요 지표
- **총 {main_col}**: {total:,.0f}
- **평균 {main_col}**: {avg:,.0f}
- **최고값**: {max_category} - {max_val:,.0f}
- **최저값**: {min_category} - {min_val:,.0f}

### 💡 핵심 인사이트
1. **상위 성과**: {max_category}가 {max_val:,.0f}로 가장 높은 수치를 기록
2. **성과 편차**: 최고값과 최저값의 차이는 {max_val - min_val:,.0f} ({((max_val - min_val) / avg * 100):.1f}%)
3. **분포 특성**: 평균 대비 {"고른 분포" if abs(max_val - avg) / avg < 0.5 else "편중된 분포"}

### 📈 권장사항
1. **{max_category}의 성공 요인 분석** 및 다른 영역에 적용
2. **{min_category}의 개선 방안** 모색
3. **성과 격차 해소**를 위한 전략 수립

### 🎯 다음 분석 제안
- 시계열 트렌드 분석
- 상관관계 분석
- 세부 카테고리별 드릴다운 분석
        """
        
        return insights.strip()


class HistoryService:
    """질문 이력 관리 서비스"""
    
    def __init__(self):
        self.history = []
        self.max_history = 50
    
    def add_question(self, question: str, success: bool = True, result: Optional[Dict] = None):
        """질문 이력 추가"""
        entry = {
            "question": question,
            "timestamp": datetime.now(),
            "success": success,
            "result": result
        }
        
        self.history.insert(0, entry)  # 최신순 정렬
        
        # 최대 개수 제한
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
    
    def get_recent_questions(self, limit: int = 5) -> List[Dict]:
        """최근 질문 목록 반환"""
        return self.history[:limit]
    
    def get_history_html(self) -> str:
        """이력을 HTML 형태로 반환"""
        if not self.history:
            return "<p>아직 질문 이력이 없습니다.</p>"
        
        html_items = []
        for item in self.history[:10]:  # 최근 10개만 표시
            status_class = "status-success" if item["success"] else "status-error"
            status_icon = "✅" if item["success"] else "❌"
            
            html_items.append(f"""
            <div class="history-item">
                <p><strong>{item["question"][:50]}{'...' if len(item["question"]) > 50 else ''}</strong></p>
                <small style="color: #6b7280;">{item["timestamp"].strftime("%Y-%m-%d %H:%M")}</small>
                <span class="{status_class}">{status_icon} {"성공" if item["success"] else "실패"}</span>
            </div>
            """)
        
        return "".join(html_items)
