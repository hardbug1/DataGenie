# DataGenie 🧞‍♂️

**LLM 기반 데이터 질의·분석·시각화 서비스**

DataGenie는 자연어를 통해 데이터베이스를 조회하고 Excel 파일을 분석하여, 인사이트와 시각화를 제공하는 AI 분석 비서입니다.

## 🌟 주요 기능

### 📊 자연어 데이터 분석
- **질문만 하면 끝**: "지난달 매출이 가장 높은 제품은?" 같은 자연어로 질문
- **스마트 분석**: GPT-4가 질문을 이해하고 적절한 SQL 쿼리나 분석 코드 생성
- **즉시 시각화**: 결과를 자동으로 차트와 그래프로 표현

### 🗄️ 다중 데이터 소스 지원
- **데이터베이스**: PostgreSQL, MySQL, SQLite 연결
- **Excel/CSV**: 파일 업로드를 통한 즉석 분석
- **안전한 접근**: 읽기 전용 연결로 데이터 안전성 보장

### 🎨 인터랙티브 웹 인터페이스
- **직관적인 UI**: Gradio 기반 사용하기 쉬운 웹 인터페이스
- **반응형 디자인**: 데스크톱과 모바일 모두 지원
- **실시간 결과**: 분석 과정과 결과를 실시간으로 확인

## 🏗️ 기술 스택

### Backend
- **FastAPI**: 고성능 비동기 웹 프레임워크
- **LangChain**: LLM 체인 및 에이전트 관리
- **SQLAlchemy**: 데이터베이스 ORM
- **OpenAI GPT-4**: 자연어 이해 및 코드 생성

### Frontend
- **Gradio**: 인터랙티브 웹 인터페이스
- **Plotly**: 인터랙티브 데이터 시각화
- **Custom CSS**: 반응형 디자인

### Database & Cache
- **PostgreSQL**: 시스템 데이터베이스
- **Redis**: 캐싱 및 세션 관리
- **External DBs**: PostgreSQL, MySQL, SQLite 지원

### Infrastructure
- **Docker**: 컨테이너화
- **Docker Compose**: 개발 환경 관리

## 🚀 빠른 시작

### 필수 요구사항
- Python 3.11+
- Docker & Docker Compose
- OpenAI API Key

### 설치 및 실행

1. **저장소 클론**
   ```bash
   git clone <repository-url>
   cd datagenie
   ```

2. **환경변수 설정**
   ```bash
   cp .env.example .env
   # .env 파일에서 OpenAI API 키 등 설정
   ```

3. **Docker로 실행**
   ```bash
   docker-compose up -d
   ```

4. **웹 인터페이스 접속**
   ```
   http://localhost:8000
   ```

## 📁 프로젝트 구조

```
datagenie/
├── app/                    # 메인 애플리케이션
│   ├── main.py            # FastAPI 진입점
│   ├── config/            # 설정 관리
│   ├── models/            # 데이터베이스 모델
│   ├── schemas/           # Pydantic 스키마
│   ├── api/v1/           # API 엔드포인트
│   ├── core/             # 핵심 비즈니스 로직
│   │   ├── nlp/          # 자연어 처리
│   │   ├── query/        # 데이터베이스 쿼리 엔진
│   │   ├── excel/        # Excel 분석 엔진
│   │   └── visualization/ # 시각화 엔진
│   ├── auth/             # 인증 & 인가
│   ├── cache/            # 캐싱 로직
│   └── utils/            # 유틸리티 함수
├── docs/                 # 프로젝트 문서
├── tests/                # 테스트 코드
├── scripts/              # 스크립트 & 마이그레이션
├── requirements/         # 의존성 관리
└── docker/              # Docker 설정
```

## 🔒 보안 원칙

- **읽기 전용 DB 접근**: 외부 데이터베이스는 읽기 전용으로만 연결
- **SQL 인젝션 방지**: 모든 쿼리는 매개변수화된 쿼리 사용
- **개인정보 보호**: 자동 PII 마스킹 및 데이터 암호화
- **인증 & 인가**: JWT 기반 사용자 인증 시스템

## 🧪 개발 및 테스트

### 개발 환경 설정
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 개발 의존성 설치
pip install -r requirements/dev.txt
```

### 테스트 실행
```bash
# 단위 테스트
pytest tests/unit/

# 통합 테스트
pytest tests/integration/

# 전체 테스트
pytest tests/
```

## 📊 사용 예시

### 데이터베이스 질의
```
질문: "지난 3개월간 월별 매출 추이를 보여주세요"
→ 자동 SQL 생성 및 실행
→ 라인 차트로 시각화
→ 인사이트 및 분석 제공
```

### Excel 분석
```
파일 업로드: sales_data.xlsx
질문: "지역별 매출 순위를 보여주세요"
→ 자동 pandas 코드 생성
→ 막대 차트로 시각화
→ 상위/하위 지역 분석
```

## 🗺️ 개발 로드맵

### MVP (v0.1.0) - 출시 예정
- [x] 프로젝트 구조 설정
- [ ] 기본 자연어 처리
- [ ] PostgreSQL 연결
- [ ] 간단한 시각화
- [ ] 기본 웹 인터페이스

### Beta (v0.5.0)
- [ ] Excel 분석 기능
- [ ] 고급 시각화
- [ ] 사용자 인증
- [ ] 모바일 반응형

### 정식 버전 (v1.0.0)
- [ ] 다중 데이터베이스 지원
- [ ] 엔터프라이즈 기능
- [ ] 성능 최적화
- [ ] 완전한 문서화

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원 및 문의

- **이슈 추적**: [GitHub Issues](./issues)
- **문서**: `/docs` 폴더 참조
- **이메일**: support@datagenie.com

---

**🧞‍♂️ DataGenie와 함께 데이터 분석의 마법을 경험해보세요!**
