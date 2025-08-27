import React, { useState } from 'react';
import './DataGeniePresentation.css';

const DataGeniePresentation = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      id: 'title',
      title: 'DataGenie 🧞‍♂️',
      subtitle: 'LLM 기반 데이터 분석 플랫폼',
      content: (
        <div className="title-slide">
          <div className="genie-icon">🧞‍♂️</div>
          <h1>DataGenie</h1>
          <h2>LLM 기반 데이터 분석 플랫폼</h2>
          <p className="tagline">자연어로 데이터를 분석하고 인사이트를 발견하세요</p>
          <div className="tech-badges">
            <span className="badge">FastAPI</span>
            <span className="badge">OpenAI GPT-4</span>
            <span className="badge">LangChain</span>
            <span className="badge">Clean Architecture</span>
          </div>
        </div>
      )
    },
    {
      id: 'overview',
      title: '프로젝트 개요',
      content: (
        <div className="overview-slide">
          <div className="overview-grid">
            <div className="overview-card">
              <div className="card-icon">🎯</div>
              <h3>목표</h3>
              <p>자연어를 통한 직관적인 데이터 분석 경험 제공</p>
            </div>
            <div className="overview-card">
              <div className="card-icon">🔧</div>
              <h3>핵심 기능</h3>
              <ul>
                <li>자연어 SQL 쿼리 생성</li>
                <li>Excel 파일 자동 분석</li>
                <li>인터랙티브 시각화</li>
                <li>다중 데이터베이스 지원</li>
              </ul>
            </div>
            <div className="overview-card">
              <div className="card-icon">🛡️</div>
              <h3>보안 원칙</h3>
              <ul>
                <li>읽기 전용 DB 접근</li>
                <li>SQL 인젝션 방지</li>
                <li>개인정보 자동 마스킹</li>
                <li>JWT 기반 인증</li>
              </ul>
            </div>
            <div className="overview-card">
              <div className="card-icon">⚡</div>
              <h3>성능</h3>
              <ul>
                <li>Redis 캐싱</li>
                <li>비동기 처리</li>
                <li>연결 풀링</li>
                <li>응답 시간 &lt; 10초</li>
              </ul>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'architecture',
      title: 'Clean Architecture 구조',
      content: (
        <div className="architecture-slide">
          <div className="architecture-diagram">
            <div className="layer presentation-layer">
              <h4>🌐 Presentation Layer</h4>
              <div className="components">
                <div className="component">Gradio Web UI</div>
                <div className="component">FastAPI REST API</div>
              </div>
            </div>
            
            <div className="layer usecase-layer">
              <h4>💼 Use Cases Layer</h4>
              <div className="components">
                <div className="component">Execute Analysis</div>
                <div className="component">Authentication</div>
                <div className="component">Data Management</div>
              </div>
            </div>
            
            <div className="layer domain-layer">
              <h4>🏛️ Domain Layer</h4>
              <div className="components">
                <div className="component">Entities</div>
                <div className="component">Value Objects</div>
                <div className="component">Interfaces</div>
              </div>
            </div>
            
            <div className="layer infrastructure-layer">
              <h4>🔧 Infrastructure Layer</h4>
              <div className="components">
                <div className="component">LLM Processor</div>
                <div className="component">Database Adapters</div>
                <div className="component">Redis Cache</div>
                <div className="component">Security</div>
              </div>
            </div>
          </div>
          
          <div className="architecture-benefits">
            <h4>Clean Architecture 장점</h4>
            <ul>
              <li>🔄 <strong>의존성 역전</strong>: 외부 의존성으로부터 비즈니스 로직 보호</li>
              <li>🧪 <strong>테스트 용이성</strong>: 각 계층별 독립적 테스트 가능</li>
              <li>🔧 <strong>유지보수성</strong>: 변경 사항의 영향 범위 최소화</li>
              <li>📈 <strong>확장성</strong>: 새로운 기능 추가 시 기존 코드 영향 최소</li>
            </ul>
          </div>
        </div>
      )
    },
    {
      id: 'tech-stack',
      title: '기술 스택',
      content: (
        <div className="tech-stack-slide">
          <div className="tech-categories">
            <div className="tech-category">
              <h4>🚀 Backend Framework</h4>
              <div className="tech-items">
                <div className="tech-item">
                  <strong>FastAPI 0.104.1</strong>
                  <span>고성능 비동기 웹 프레임워크</span>
                </div>
                <div className="tech-item">
                  <strong>Uvicorn 0.24.0</strong>
                  <span>ASGI 서버</span>
                </div>
                <div className="tech-item">
                  <strong>Pydantic 2.5.0</strong>
                  <span>데이터 검증 및 타입 안전성</span>
                </div>
              </div>
            </div>
            
            <div className="tech-category">
              <h4>🤖 AI & LLM</h4>
              <div className="tech-items">
                <div className="tech-item">
                  <strong>OpenAI ≥1.6.1</strong>
                  <span>GPT-4 통합</span>
                </div>
                <div className="tech-item">
                  <strong>LangChain 0.0.340</strong>
                  <span>SQL 에이전트 및 체인 관리</span>
                </div>
                <div className="tech-item">
                  <strong>TikToken ≥0.5.2</strong>
                  <span>토큰 계산 및 비용 최적화</span>
                </div>
              </div>
            </div>
            
            <div className="tech-category">
              <h4>🗄️ Database</h4>
              <div className="tech-items">
                <div className="tech-item">
                  <strong>SQLAlchemy 2.0.23</strong>
                  <span>ORM 및 연결 풀링</span>
                </div>
                <div className="tech-item">
                  <strong>AsyncPG / AioMySQL</strong>
                  <span>비동기 데이터베이스 드라이버</span>
                </div>
                <div className="tech-item">
                  <strong>Alembic 1.12.1</strong>
                  <span>데이터베이스 마이그레이션</span>
                </div>
              </div>
            </div>
            
            <div className="tech-category">
              <h4>📊 Data & Visualization</h4>
              <div className="tech-items">
                <div className="tech-item">
                  <strong>Pandas 2.1.4</strong>
                  <span>데이터 조작 및 분석</span>
                </div>
                <div className="tech-item">
                  <strong>Plotly 5.17.0</strong>
                  <span>인터랙티브 시각화</span>
                </div>
                <div className="tech-item">
                  <strong>Gradio 4.8.0</strong>
                  <span>웹 인터페이스</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'data-flow',
      title: '데이터 플로우',
      content: (
        <div className="data-flow-slide">
          <div className="flow-diagram">
            <div className="flow-step">
              <div className="step-icon">👤</div>
              <div className="step-content">
                <h4>사용자 입력</h4>
                <p>자연어 질문 또는 Excel 파일</p>
              </div>
            </div>
            
            <div className="flow-arrow">→</div>
            
            <div className="flow-step">
              <div className="step-icon">🧠</div>
              <div className="step-content">
                <h4>자연어 처리</h4>
                <p>GPT-4를 통한 의도 분석</p>
              </div>
            </div>
            
            <div className="flow-arrow">→</div>
            
            <div className="flow-branch">
              <div className="branch-option">
                <div className="step-icon">🗄️</div>
                <div className="step-content">
                  <h4>DB 쿼리</h4>
                  <p>SQL 생성 및 실행</p>
                </div>
              </div>
              
              <div className="branch-option">
                <div className="step-icon">📊</div>
                <div className="step-content">
                  <h4>Excel 분석</h4>
                  <p>Pandas 코드 생성</p>
                </div>
              </div>
            </div>
            
            <div className="flow-arrow">→</div>
            
            <div className="flow-step">
              <div className="step-icon">📈</div>
              <div className="step-content">
                <h4>시각화</h4>
                <p>Plotly 차트 생성</p>
              </div>
            </div>
            
            <div className="flow-arrow">→</div>
            
            <div className="flow-step">
              <div className="step-icon">🎨</div>
              <div className="step-content">
                <h4>결과 출력</h4>
                <p>Gradio UI를 통한 표시</p>
              </div>
            </div>
          </div>
          
          <div className="flow-features">
            <div className="feature">
              <h4>⚡ 캐싱 전략</h4>
              <ul>
                <li>Redis를 통한 쿼리 결과 캐싱</li>
                <li>LLM 응답 캐싱으로 비용 절약</li>
                <li>세션 데이터 관리</li>
              </ul>
            </div>
            
            <div className="feature">
              <h4>🛡️ 보안 검증</h4>
              <ul>
                <li>SQL 인젝션 방지</li>
                <li>위험한 Python 코드 차단</li>
                <li>개인정보 자동 마스킹</li>
              </ul>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'llm-integration',
      title: 'LLM 통합 전략',
      content: (
        <div className="llm-slide">
          <div className="llm-components">
            <div className="llm-component">
              <h4>🤖 LLM Processor</h4>
              <div className="component-details">
                <p><strong>주요 기능:</strong></p>
                <ul>
                  <li>자연어 질문 분석 및 분류</li>
                  <li>SQL 쿼리 자동 생성</li>
                  <li>Python 코드 생성 (Excel 분석)</li>
                  <li>결과 해석 및 인사이트 제공</li>
                </ul>
              </div>
            </div>
            
            <div className="llm-component">
              <h4>🔗 LangChain 활용</h4>
              <div className="component-details">
                <p><strong>구현 요소:</strong></p>
                <ul>
                  <li>SQL Database Agent</li>
                  <li>프롬프트 템플릿 관리</li>
                  <li>체인 기반 워크플로우</li>
                  <li>도구 통합 (Tool Integration)</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="prompt-strategy">
            <h4>📝 프롬프트 엔지니어링</h4>
            <div className="prompt-examples">
              <div className="prompt-example">
                <h5>SQL 생성 프롬프트</h5>
                <div className="code-block">
                  <pre>{`당신은 DataGenie의 전문 SQL 분석가입니다.

중요 규칙:
- SELECT 쿼리만 생성 (INSERT/UPDATE/DELETE 금지)
- 매개변수화된 쿼리로 SQL 인젝션 방지
- 결과를 최대 1000행으로 제한
- 개인정보 자동 마스킹 고려

사용자 질문: {question}
데이터베이스 스키마: {schema_info}

응답 형식 (JSON):
{
  "sql": "SELECT ...",
  "explanation": "쿼리 설명",
  "confidence": 0.95,
  "warnings": ["주의사항"]
}`}</pre>
                </div>
              </div>
            </div>
          </div>
          
          <div className="llm-benefits">
            <h4>💡 LLM 통합 장점</h4>
            <div className="benefits-grid">
              <div className="benefit">
                <strong>🎯 정확성</strong>
                <p>구조화된 프롬프트로 일관된 결과</p>
              </div>
              <div className="benefit">
                <strong>🛡️ 안전성</strong>
                <p>프롬프트 인젝션 방지 및 출력 검증</p>
              </div>
              <div className="benefit">
                <strong>💰 비용 효율</strong>
                <p>캐싱과 토큰 최적화</p>
              </div>
              <div className="benefit">
                <strong>🔄 확장성</strong>
                <p>새로운 데이터 소스 쉽게 추가</p>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'security',
      title: '보안 아키텍처',
      content: (
        <div className="security-slide">
          <div className="security-layers">
            <div className="security-layer">
              <h4>🔐 인증 & 인가</h4>
              <div className="security-details">
                <ul>
                  <li><strong>JWT 토큰 기반 인증</strong></li>
                  <li>사용자별 권한 관리</li>
                  <li>세션 타임아웃 제어</li>
                  <li>API 엔드포인트 보호</li>
                </ul>
              </div>
            </div>
            
            <div className="security-layer">
              <h4>🛡️ SQL 보안</h4>
              <div className="security-details">
                <ul>
                  <li><strong>SQL 인젝션 방지</strong></li>
                  <li>위험한 명령어 필터링</li>
                  <li>매개변수화된 쿼리 강제</li>
                  <li>읽기 전용 데이터베이스 연결</li>
                </ul>
              </div>
            </div>
            
            <div className="security-layer">
              <h4>🔒 데이터 보호</h4>
              <div className="security-details">
                <ul>
                  <li><strong>개인정보 자동 마스킹</strong></li>
                  <li>민감 데이터 암호화</li>
                  <li>로그 데이터 익명화</li>
                  <li>GDPR 준수</li>
                </ul>
              </div>
            </div>
            
            <div className="security-layer">
              <h4>🚫 코드 실행 보안</h4>
              <div className="security-details">
                <ul>
                  <li><strong>Python 코드 검증</strong></li>
                  <li>파일 시스템 접근 차단</li>
                  <li>네트워크 요청 금지</li>
                  <li>시스템 호출 방지</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="security-implementation">
            <h4>🔧 보안 구현 예시</h4>
            <div className="code-example">
              <pre>{`class SQLValidator:
    FORBIDDEN_KEYWORDS = [
        'DROP', 'DELETE', 'INSERT', 'UPDATE', 
        'ALTER', 'CREATE', 'TRUNCATE'
    ]
    
    def validate_sql(self, sql: str) -> bool:
        # SQL 파싱 및 위험 명령어 검사
        parsed = sqlparse.parse(sql)
        for statement in parsed:
            if self._contains_forbidden_keywords(statement):
                raise ValueError("위험한 SQL 명령어 감지")
        return True`}</pre>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'performance',
      title: '성능 최적화',
      content: (
        <div className="performance-slide">
          <div className="performance-metrics">
            <div className="metric-card">
              <div className="metric-value">< 10초</div>
              <div className="metric-label">평균 응답 시간</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">100명</div>
              <div className="metric-label">동시 사용자</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">95%</div>
              <div className="metric-label">캐시 히트율</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">< 1%</div>
              <div className="metric-label">에러율</div>
            </div>
          </div>
          
          <div className="optimization-strategies">
            <div className="strategy">
              <h4>⚡ 캐싱 전략</h4>
              <ul>
                <li><strong>Redis 다층 캐싱</strong></li>
                <li>쿼리 결과 캐싱 (TTL: 1시간)</li>
                <li>LLM 응답 캐싱 (비용 절약)</li>
                <li>세션 데이터 캐싱</li>
              </ul>
            </div>
            
            <div className="strategy">
              <h4>🔄 비동기 처리</h4>
              <ul>
                <li><strong>FastAPI 비동기 지원</strong></li>
                <li>데이터베이스 비동기 드라이버</li>
                <li>HTTP 클라이언트 비동기</li>
                <li>파일 I/O 비동기</li>
              </ul>
            </div>
            
            <div className="strategy">
              <h4>🗄️ 데이터베이스 최적화</h4>
              <ul>
                <li><strong>연결 풀링</strong></li>
                <li>쿼리 타임아웃 설정</li>
                <li>인덱스 활용 권장</li>
                <li>결과셋 크기 제한</li>
              </ul>
            </div>
            
            <div className="strategy">
              <h4>💰 비용 최적화</h4>
              <ul>
                <li><strong>토큰 사용량 모니터링</strong></li>
                <li>프롬프트 길이 최적화</li>
                <li>응답 캐싱으로 재사용</li>
                <li>폴백 모델 활용</li>
              </ul>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'demo',
      title: '사용 예시',
      content: (
        <div className="demo-slide">
          <div className="demo-scenarios">
            <div className="demo-scenario">
              <h4>📊 데이터베이스 질의</h4>
              <div className="demo-flow">
                <div className="demo-step">
                  <strong>사용자 질문:</strong>
                  <div className="question">"지난 3개월간 월별 매출 추이를 보여주세요"</div>
                </div>
                <div className="demo-arrow">↓</div>
                <div className="demo-step">
                  <strong>자동 생성된 SQL:</strong>
                  <div className="code-block">
                    <pre>{`SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(total_amount) as monthly_revenue
FROM orders 
WHERE order_date >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;`}</pre>
                  </div>
                </div>
                <div className="demo-arrow">↓</div>
                <div className="demo-step">
                  <strong>결과:</strong>
                  <div className="result">📈 라인 차트로 시각화 + 인사이트 제공</div>
                </div>
              </div>
            </div>
            
            <div className="demo-scenario">
              <h4>📁 Excel 분석</h4>
              <div className="demo-flow">
                <div className="demo-step">
                  <strong>파일 업로드:</strong>
                  <div className="question">sales_data.xlsx</div>
                </div>
                <div className="demo-arrow">↓</div>
                <div className="demo-step">
                  <strong>사용자 질문:</strong>
                  <div className="question">"지역별 매출 순위를 보여주세요"</div>
                </div>
                <div className="demo-arrow">↓</div>
                <div className="demo-step">
                  <strong>자동 생성된 코드:</strong>
                  <div className="code-block">
                    <pre>{`# 지역별 매출 집계 및 정렬
region_sales = df.groupby('region')['sales'].sum()
region_sales_sorted = region_sales.sort_values(ascending=False)
print(region_sales_sorted)`}</pre>
                  </div>
                </div>
                <div className="demo-arrow">↓</div>
                <div className="demo-step">
                  <strong>결과:</strong>
                  <div className="result">📊 막대 차트 + 상위/하위 지역 분석</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'roadmap',
      title: '개발 로드맵',
      content: (
        <div className="roadmap-slide">
          <div className="roadmap-timeline">
            <div className="timeline-item completed">
              <div className="timeline-marker">✅</div>
              <div className="timeline-content">
                <h4>Phase 1: 기반 구조 (완료)</h4>
                <ul>
                  <li>Clean Architecture 구현</li>
                  <li>FastAPI 백엔드 구축</li>
                  <li>Docker 컨테이너화</li>
                  <li>기본 보안 구현</li>
                </ul>
              </div>
            </div>
            
            <div className="timeline-item completed">
              <div className="timeline-marker">✅</div>
              <div className="timeline-content">
                <h4>Phase 2: 핵심 기능 (완료)</h4>
                <ul>
                  <li>OpenAI LLM 통합</li>
                  <li>자연어 처리 모듈</li>
                  <li>SQL 생성 엔진</li>
                  <li>Excel 분석 엔진</li>
                  <li>시각화 엔진</li>
                </ul>
              </div>
            </div>
            
            <div className="timeline-item current">
              <div className="timeline-marker">🔄</div>
              <div className="timeline-content">
                <h4>Phase 3: 고도화 (진행중)</h4>
                <ul>
                  <li>고급 시각화 기능</li>
                  <li>사용자 인증 시스템</li>
                  <li>성능 최적화</li>
                  <li>모바일 반응형 UI</li>
                </ul>
              </div>
            </div>
            
            <div className="timeline-item future">
              <div className="timeline-marker">📅</div>
              <div className="timeline-content">
                <h4>Phase 4: 엔터프라이즈 (계획)</h4>
                <ul>
                  <li>다중 데이터베이스 지원 확대</li>
                  <li>실시간 데이터 스트리밍</li>
                  <li>대시보드 기능</li>
                  <li>API 확장</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="roadmap-stats">
            <div className="stat">
              <div className="stat-number">85%</div>
              <div className="stat-label">전체 진행률</div>
            </div>
            <div className="stat">
              <div className="stat-number">2개월</div>
              <div className="stat-label">MVP 개발 기간</div>
            </div>
            <div className="stat">
              <div className="stat-number">100%</div>
              <div className="stat-label">테스트 커버리지 목표</div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'conclusion',
      title: '결론 및 향후 계획',
      content: (
        <div className="conclusion-slide">
          <div className="achievements">
            <h4>🎉 주요 성과</h4>
            <div className="achievement-grid">
              <div className="achievement">
                <div className="achievement-icon">🏗️</div>
                <h5>견고한 아키텍처</h5>
                <p>Clean Architecture 기반의 확장 가능한 구조</p>
              </div>
              <div className="achievement">
                <div className="achievement-icon">🤖</div>
                <h5>LLM 통합</h5>
                <p>GPT-4와 LangChain을 활용한 지능형 분석</p>
              </div>
              <div className="achievement">
                <div className="achievement-icon">🛡️</div>
                <h5>보안 강화</h5>
                <p>다층 보안 체계로 안전한 데이터 처리</p>
              </div>
              <div className="achievement">
                <div className="achievement-icon">⚡</div>
                <h5>고성능</h5>
                <p>비동기 처리와 캐싱으로 빠른 응답</p>
              </div>
            </div>
          </div>
          
          <div className="next-steps">
            <h4>🚀 향후 계획</h4>
            <div className="next-step-cards">
              <div className="next-step-card">
                <h5>단기 (1-2개월)</h5>
                <ul>
                  <li>사용자 피드백 수집 및 반영</li>
                  <li>성능 모니터링 및 최적화</li>
                  <li>추가 데이터 소스 지원</li>
                </ul>
              </div>
              <div className="next-step-card">
                <h5>중기 (3-6개월)</h5>
                <ul>
                  <li>엔터프라이즈 기능 개발</li>
                  <li>대시보드 및 리포팅</li>
                  <li>API 생태계 구축</li>
                </ul>
              </div>
              <div className="next-step-card">
                <h5>장기 (6개월+)</h5>
                <ul>
                  <li>AI 모델 자체 개발</li>
                  <li>실시간 분석 플랫폼</li>
                  <li>글로벌 서비스 확장</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="call-to-action">
            <h4>💡 DataGenie와 함께 데이터 분석의 미래를 만들어보세요!</h4>
            <div className="cta-buttons">
              <button className="cta-button primary">GitHub 저장소</button>
              <button className="cta-button secondary">데모 체험</button>
              <button className="cta-button secondary">문서 보기</button>
            </div>
          </div>
        </div>
      )
    }
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  return (
    <div className="presentation-container">
      <div className="slide-content">
        {slides[currentSlide].content}
      </div>
      
      <div className="presentation-controls">
        <button onClick={prevSlide} disabled={currentSlide === 0}>
          ← 이전
        </button>
        
        <div className="slide-indicators">
          {slides.map((_, index) => (
            <button
              key={index}
              className={`indicator ${index === currentSlide ? 'active' : ''}`}
              onClick={() => goToSlide(index)}
            >
              {index + 1}
            </button>
          ))}
        </div>
        
        <button onClick={nextSlide} disabled={currentSlide === slides.length - 1}>
          다음 →
        </button>
      </div>
      
      <div className="slide-counter">
        {currentSlide + 1} / {slides.length}
      </div>
    </div>
  );
};

export default DataGeniePresentation;
