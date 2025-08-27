# DataGenie 개발 체크리스트

## 📋 프로젝트 개요
- **프로젝트명**: DataGenie (LLM 기반 데이터 질의·분석·시각화 서비스)
- **기술 스택**: Python, FastAPI, LangChain, Gradio, PostgreSQL, Redis
- **개발 기간**: MVP 2개월, 정식 버전 4개월

## 🚀 Phase 1: 프로젝트 초기 설정 (1주차)

### 📁 1.1 프로젝트 구조 생성
- [x] 프로젝트 루트 디렉터리 생성
- [x] 기본 폴더 구조 생성
  ```
  datagenie/
  ├── app/
  ├── docs/
  ├── tests/
  ├── scripts/
  ├── requirements/
  └── docker/
  ```
- [x] `.gitignore` 파일 생성 (Python, IDE, 환경변수 등)
- [x] `README.md` 기본 내용 작성
- [x] **🔄 커밋**: `feat: 프로젝트 초기 구조 설정` ✅ 완료

### ⚙️ 1.2 개발 환경 설정
- [x] Python 3.11+ 가상환경 생성
  ```bash
  python -m venv venv
  source venv/bin/activate  # macOS/Linux
  ```
- [x] 기본 의존성 파일 생성
  - [x] `requirements/base.txt` - 기본 패키지
  - [x] `requirements/dev.txt` - 개발용 패키지
  - [x] `requirements/prod.txt` - 운영용 패키지
- [x] 환경변수 파일 설정
  - [x] `env.example` 템플릿 생성
  - [x] `.env` 파일 생성 (gitignore에 포함)
- [x] **🔄 커밋**: `feat: 개발 환경 설정 및 의존성 정의` ✅ 완료

### 🐳 1.3 Docker 설정
- [x] `Dockerfile` 작성
- [x] `docker-compose.yml` 작성 (app, postgres, redis)
- [x] `docker-compose.dev.yml` 개발용 설정
- [x] Docker 빌드 및 실행 테스트
- [x] **🔄 커밋**: `feat: Docker 컨테이너 설정` ✅ 완료

### 📊 1.4 데이터베이스 초기 설정
- [x] PostgreSQL 컨테이너 실행 확인
- [x] Redis 컨테이너 실행 확인
- [x] 데이터베이스 연결 테스트
- [x] **🔄 커밋**: `feat: 데이터베이스 컨테이너 설정` ✅ 완료

## 🏗️ Phase 2: 백엔드 기본 구조 (2주차)

### 🔧 2.1 FastAPI 애플리케이션 구조
- [x] FastAPI 앱 기본 구조 생성
  ```
  app/
  ├── main.py
  ├── config/
  │   ├── settings.py
  │   └── database.py
  ├── models/
  ├── schemas/
  ├── api/
  │   └── v1/
  ├── domain/
  ├── use_cases/
  ├── infrastructure/
  └── utils/
  ```
- [x] 설정 관리 시스템 구현 (`pydantic.BaseSettings`)
- [x] 로깅 설정 구현
- [x] **🔄 커밋**: `feat: FastAPI 기본 애플리케이션 구조` ✅ 완료

### 🗄️ 2.2 데이터베이스 모델 및 마이그레이션
- [x] SQLAlchemy 모델 정의
  - [x] `User` 모델
  - [x] `DatabaseConnection` 모델
  - [x] `QueryHistory` 모델
  - [x] `UserSession` 모델
- [x] Alembic 마이그레이션 설정
- [x] 초기 마이그레이션 파일 생성
- [x] 데이터베이스 스키마 생성 테스트
- [x] **🔄 커밋**: `feat: 데이터베이스 모델 및 마이그레이션 설정` ✅ 완료

### 🔐 2.3 인증 시스템
- [x] JWT 토큰 생성/검증 유틸리티 (Mock 구현)
- [x] 사용자 인증 미들웨어
- [x] 로그인/로그아웃 API 엔드포인트 (계획됨)
- [x] 비밀번호 해싱 (bcrypt) (계획됨)
- [x] 토큰 갱신 로직 (계획됨)
- [x] **🔄 커밋**: `feat: JWT 기반 사용자 인증 시스템` ✅ Mock 완료

### 📡 2.4 기본 API 엔드포인트
- [x] 헬스체크 API (`/health`)
- [x] 사용자 관리 API (`/users`) (계획됨)
- [x] 인증 API (`/auth`) (Mock 구현)
- [x] API 문서 자동 생성 (Swagger UI)
- [x] CORS 설정
- [x] **🔄 커밋**: `feat: 기본 API 엔드포인트 및 문서화` ✅ 완료

### 🏛️ 2.5 Clean Architecture 구현
- [x] Domain 계층 구현
  - [x] `AnalysisQuery` 엔티티
  - [x] `AnalysisResult` 값 객체
  - [x] 도메인 인터페이스 정의
- [x] Use Cases 계층 구현
  - [x] `ExecuteAnalysisUseCase` 구현
  - [x] 비즈니스 로직 분리
- [x] Infrastructure 계층 구현
  - [x] 의존성 주입 컨테이너
  - [x] Mock 구현체들 (개발용)
  - [x] Repository 어댑터
- [x] API 계층 구현
  - [x] 분석 실행 엔드포인트
  - [x] 파일 업로드 엔드포인트
  - [x] Pydantic 스키마
- [x] **🔄 커밋**: `feat: Clean Architecture 기반 핵심 구조 구현` ✅ 완료

## 🧠 Phase 3: 핵심 분석 엔진 (3-4주차)

### 🤖 3.1 LLM 통합
- [ ] OpenAI API 클라이언트 설정
- [ ] LangChain 기본 설정
- [ ] 프롬프트 템플릿 관리 시스템
- [ ] LLM 응답 캐싱 (Redis)
- [ ] 에러 핸들링 및 재시도 로직
- [ ] **🔄 커밋**: `feat: OpenAI LLM 통합 및 LangChain 설정`

### 🔍 3.2 자연어 처리 모듈
- [ ] 질문 분석 및 분류 로직
  ```python
  class NLPProcessor:
      def analyze_question(self, question: str) -> QuestionAnalysis
      def classify_intent(self, question: str) -> str
      def extract_entities(self, question: str) -> Dict
  ```
- [ ] 질문 유형 분류 (DB_QUERY, EXCEL_ANALYSIS, GENERAL)
- [ ] 엔티티 추출 (날짜, 수치, 카테고리 등)
- [ ] 컨텍스트 관리 (이전 질문 참조)
- [ ] **🔄 커밋**: `feat: 자연어 처리 및 질문 분석 모듈`

### 🗄️ 3.3 데이터베이스 쿼리 엔진
- [ ] 데이터베이스 연결 관리자
  ```python
  class ConnectionManager:
      def create_connection_pool(self, config: Dict) -> Engine
      def get_schema_info(self, connection_id: str) -> Dict
  ```
- [ ] LangChain SQL Agent 설정
- [ ] SQL 생성 및 실행 로직
- [ ] 쿼리 결과 후처리 (개인정보 마스킹)
- [ ] SQL 인젝션 방지 검증
- [ ] **🔄 커밋**: `feat: 데이터베이스 쿼리 엔진 및 SQL Agent`

### 📁 3.4 Excel 분석 엔진
- [ ] 파일 업로드 처리
  ```python
  class ExcelEngine:
      def process_file(self, file_data: bytes) -> Dict
      def analyze_data(self, question: str, file_id: str) -> Dict
  ```
- [ ] Excel/CSV 파일 파싱 (pandas)
- [ ] 스키마 자동 감지
- [ ] Pandas 코드 생성 (LLM 기반)
- [ ] 안전한 코드 실행 환경
- [ ] **🔄 커밋**: `feat: Excel 파일 분석 엔진`

### 📊 3.5 시각화 엔진
- [ ] 차트 유형 자동 추천 로직
  ```python
  class VisualizationEngine:
      def recommend_chart_type(self, data: DataFrame) -> str
      def create_chart(self, data: DataFrame, chart_type: str) -> Dict
  ```
- [ ] Plotly 차트 생성
- [ ] 차트 설정 최적화 (한글 폰트, 색상 테마)
- [ ] 인터랙티브 기능 (확대/축소, 필터링)
- [ ] 차트 내보내기 (PNG, SVG, HTML)
- [ ] **🔄 커밋**: `feat: Plotly 기반 시각화 엔진`

## 🎨 Phase 4: 프론트엔드 UI (5주차)

### 🖥️ 4.1 Gradio 기본 인터페이스
- [ ] Gradio 앱 기본 구조
  ```python
  def create_app():
      with gr.Blocks(theme=gr.themes.Soft()) as app:
          # 인터페이스 구성
      return app
  ```
- [ ] 커스텀 CSS 스타일 적용
- [ ] 반응형 레이아웃 설정
- [ ] **🔄 커밋**: `feat: Gradio 기본 인터페이스 구조`

### 📝 4.2 질문 입력 컴포넌트
- [ ] 질문 입력 텍스트박스
- [ ] 예시 질문 버튼들
- [ ] 파일 업로드 컴포넌트
- [ ] 데이터 소스 선택 탭
- [ ] 입력 검증 및 피드백
- [ ] **🔄 커밋**: `feat: 질문 입력 및 데이터 소스 선택 UI`

### 📊 4.3 결과 표시 컴포넌트
- [ ] 로딩 상태 표시
- [ ] 인사이트 카드 컴포넌트
- [ ] 차트 표시 영역
- [ ] 데이터 테이블 컴포넌트
- [ ] 탭 기반 결과 구성
- [ ] **🔄 커밋**: `feat: 분석 결과 표시 UI 컴포넌트`

### 🔧 4.4 사이드바 및 네비게이션
- [ ] 질문 이력 사이드바
- [ ] 즐겨찾기 관리
- [ ] 빠른 설정 패널
- [ ] 모바일 반응형 사이드바
- [ ] **🔄 커밋**: `feat: 사이드바 및 네비게이션 UI`

## 🔗 Phase 5: API 통합 (6주차)

### 📡 5.1 API 엔드포인트 완성
- [ ] 분석 실행 API (`/api/v1/analysis/execute`)
- [ ] Excel 분석 API (`/api/v1/excel/analyze`)
- [ ] 질문 이력 API (`/api/v1/history`)
- [ ] 시각화 API (`/api/v1/visualization`)
- [ ] **🔄 커밋**: `feat: 분석 및 시각화 API 엔드포인트`

### 🔄 5.2 프론트엔드-백엔드 연동
- [ ] Gradio에서 API 호출 로직
- [ ] 비동기 요청 처리
- [ ] 에러 상태 처리
- [ ] 로딩 상태 관리
- [ ] 실시간 진행 상황 표시
- [ ] **🔄 커밋**: `feat: 프론트엔드-백엔드 API 통합`

### ⚡ 5.3 캐싱 및 성능 최적화
- [ ] Redis 캐싱 전략 구현
- [ ] 쿼리 결과 캐싱
- [ ] LLM 응답 캐싱
- [ ] 스키마 정보 캐싱
- [ ] 캐시 무효화 로직
- [ ] **🔄 커밋**: `feat: Redis 캐싱 시스템 및 성능 최적화`

## 🧪 Phase 6: 테스트 및 품질 보증 (7주차)

### 🔬 6.1 단위 테스트
- [ ] 백엔드 유닛 테스트 (pytest)
  - [ ] NLP 프로세서 테스트
  - [ ] 쿼리 엔진 테스트
  - [ ] Excel 엔진 테스트
  - [ ] 시각화 엔진 테스트
- [ ] 테스트 커버리지 80% 이상 달성
- [ ] **🔄 커밋**: `test: 백엔드 핵심 모듈 단위 테스트`

### 🔄 6.2 통합 테스트
- [ ] API 엔드포인트 테스트
- [ ] 데이터베이스 연동 테스트
- [ ] 파일 업로드/처리 테스트
- [ ] 인증 및 권한 테스트
- [ ] **🔄 커밋**: `test: API 및 시스템 통합 테스트`

### 🚀 6.3 E2E 테스트
- [ ] 전체 분석 워크플로우 테스트
- [ ] 사용자 시나리오 기반 테스트
- [ ] 브라우저 호환성 테스트
- [ ] 모바일 반응형 테스트
- [ ] **🔄 커밋**: `test: E2E 테스트 및 사용자 시나리오 검증`

### 🛡️ 6.4 보안 및 성능 테스트
- [ ] SQL 인젝션 취약점 테스트
- [ ] 인증/인가 보안 테스트
- [ ] 파일 업로드 보안 테스트
- [ ] 부하 테스트 (동시 사용자 10명)
- [ ] 메모리 누수 테스트
- [ ] **🔄 커밋**: `test: 보안 및 성능 테스트`

## 🚢 Phase 7: 배포 준비 (8주차)

### 🐳 7.1 운영 환경 설정
- [ ] 운영용 Docker 이미지 최적화
- [ ] 환경별 설정 분리 (dev/staging/prod)
- [ ] 시크릿 관리 (환경변수, Docker secrets)
- [ ] 로그 수집 설정
- [ ] **🔄 커밋**: `deploy: 운영 환경 Docker 설정`

### 📊 7.2 모니터링 및 로깅
- [ ] 구조화된 로깅 설정 (structlog)
- [ ] 헬스체크 엔드포인트 강화
- [ ] 메트릭 수집 (Prometheus)
- [ ] 에러 추적 시스템
- [ ] **🔄 커밋**: `feat: 모니터링 및 로깅 시스템`

### 🔒 7.3 보안 강화
- [ ] HTTPS 설정
- [ ] 보안 헤더 설정
- [ ] Rate Limiting 구현
- [ ] API 키 관리
- [ ] 데이터 암호화 (연결 정보)
- [ ] **🔄 커밋**: `security: 운영 보안 설정 강화`

### 📚 7.4 문서화 완성
- [ ] API 문서 완성 (OpenAPI)
- [ ] 사용자 가이드 작성
- [ ] 관리자 매뉴얼 작성
- [ ] 트러블슈팅 가이드
- [ ] **🔄 커밋**: `docs: 운영 문서 및 사용자 가이드 완성`

## 🎯 Phase 8: MVP 출시 및 피드백 (9-10주차)

### 🚀 8.1 MVP 배포
- [ ] 스테이징 환경 배포 테스트
- [ ] 운영 환경 초기 배포
- [ ] 데이터베이스 마이그레이션
- [ ] 초기 사용자 계정 생성
- [ ] **🔄 커밋**: `deploy: MVP 운영 환경 배포`

### 👥 8.2 사용자 테스트
- [ ] 내부 사용자 테스트 (개발팀)
- [ ] 베타 사용자 테스트 (5-10명)
- [ ] 피드백 수집 및 분석
- [ ] 긴급 버그 수정
- [ ] **🔄 커밋**: `fix: 사용자 피드백 기반 버그 수정`

### 📈 8.3 모니터링 및 최적화
- [ ] 실사용 데이터 분석
- [ ] 성능 병목 지점 파악
- [ ] 사용자 행동 패턴 분석
- [ ] 시스템 안정성 모니터링
- [ ] **🔄 커밋**: `perf: 실사용 데이터 기반 성능 최적화`

## 🔄 Phase 9: 정식 버전 개발 (11-16주차)

### ✨ 9.1 고급 기능 개발
- [ ] 대시보드 기능
- [ ] 스케줄링된 분석
- [ ] 고급 시각화 (히트맵, 산점도)
- [ ] 데이터 내보내기 강화
- [ ] **🔄 커밋**: `feat: 고급 분석 및 대시보드 기능`

### 🏢 9.2 엔터프라이즈 기능
- [ ] 다중 조직 지원
- [ ] 역할 기반 권한 관리
- [ ] SSO 통합
- [ ] 감사 로그 강화
- [ ] **🔄 커밋**: `feat: 엔터프라이즈 사용자 관리`

### 🔌 9.3 확장성 개선
- [ ] 수평 확장 지원
- [ ] 로드 밸런싱
- [ ] 데이터베이스 클러스터링
- [ ] CDN 설정
- [ ] **🔄 커밋**: `feat: 시스템 확장성 및 성능 개선`

### 📱 9.4 모바일 최적화
- [ ] PWA (Progressive Web App) 설정
- [ ] 오프라인 기능
- [ ] 푸시 알림
- [ ] 모바일 UX 개선
- [ ] **🔄 커밋**: `feat: PWA 및 모바일 최적화`

## 🏁 Phase 10: 정식 출시 (17-18주차)

### 🎉 10.1 정식 버전 출시
- [ ] 최종 품질 검증
- [ ] 운영 환경 스케일링
- [ ] 백업 및 복구 시스템 점검
- [ ] 출시 공지 준비
- [ ] **🔄 커밋**: `release: v1.0.0 정식 버전 출시`

### 📖 10.2 출시 후 지원
- [ ] 사용자 온보딩 지원
- [ ] 기술 지원 체계 구축
- [ ] 지속적 모니터링
- [ ] 피드백 수집 시스템
- [ ] **🔄 커밋**: `support: 출시 후 사용자 지원 체계`

## 📋 일일/주간 체크리스트

### 📅 일일 체크리스트
- [ ] 코드 리뷰 완료
- [ ] 테스트 통과 확인
- [ ] 커밋 메시지 컨벤션 준수
- [ ] 문서 업데이트
- [ ] 보안 이슈 점검

### 📆 주간 체크리스트
- [ ] 주간 진행 상황 리뷰
- [ ] 다음 주 작업 계획 수립
- [ ] 기술 부채 정리
- [ ] 성능 메트릭 점검
- [ ] 사용자 피드백 검토

## 🔧 커밋 메시지 컨벤션

### 📝 커밋 타입
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅
- `refactor`: 코드 리팩터링
- `test`: 테스트 추가/수정
- `chore`: 기타 작업
- `deploy`: 배포 관련
- `security`: 보안 관련
- `perf`: 성능 개선

### 📋 커밋 메시지 형식
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 예시
```
feat(auth): JWT 기반 사용자 인증 시스템 구현

- JWT 토큰 생성 및 검증 로직
- 비밀번호 해싱 (bcrypt)
- 토큰 갱신 API 엔드포인트

Closes #12
```

## 🎯 마일스톤 및 릴리즈

### 🏃‍♂️ MVP (v0.1.0) - 2개월 후
- [ ] 기본 질문-답변 기능
- [ ] PostgreSQL 연결
- [ ] 간단한 시각화
- [ ] 기본 웹 인터페이스

### 🚀 Beta (v0.5.0) - 3개월 후
- [ ] Excel 분석 기능
- [ ] 고급 시각화
- [ ] 사용자 인증
- [ ] 모바일 반응형

### 🎉 정식 버전 (v1.0.0) - 4개월 후
- [ ] 전체 기능 완성
- [ ] 엔터프라이즈 기능
- [ ] 성능 최적화
- [ ] 완전한 문서화

---

## 📞 지원 및 문의

프로젝트 진행 중 문제가 발생하거나 추가 기능이 필요한 경우:

1. **이슈 추적**: GitHub Issues 활용
2. **문서 참조**: `/docs` 폴더의 설계 문서
3. **코드 리뷰**: Pull Request 템플릿 사용
4. **배포 가이드**: Docker Compose 및 환경설정 문서

**성공적인 DataGenie 프로젝트 완성을 위해 체계적으로 진행해보세요! 🎯**
