# DataGenie API 명세서

## 📋 문서 정보
- **프로젝트명**: DataGenie (LLM 기반 데이터 질의·분석·시각화 서비스)
- **작성일**: 2024년
- **버전**: 1.0
- **API 버전**: v1

## 🎯 API 개요

### 설계 원칙
- **RESTful 아키텍처**: 표준 HTTP 메서드 사용
- **JSON 기반**: 모든 요청/응답은 JSON 형식
- **버전 관리**: URL 경로에 버전 명시 (/api/v1/)
- **보안 우선**: JWT 토큰 기반 인증
- **표준화된 오류**: 일관된 오류 응답 형식

### 기본 정보
- **Base URL**: `https://api.datagenie.com/api/v1`
- **Content-Type**: `application/json`
- **인증 방식**: Bearer Token (JWT)
- **Rate Limiting**: 사용자당 분당 100회 요청

## 🔐 인증 및 보안

### 1. JWT 토큰 구조

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_uuid",
    "username": "user123",
    "role": "user",
    "permissions": ["query:read", "excel:analyze"],
    "iat": 1640995200,
    "exp": 1641081600
  }
}
```

### 2. 인증 헤더
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
X-Request-ID: <UUID> (선택사항, 요청 추적용)
```

### 3. 권한 레벨
- **admin**: 모든 기능 접근
- **user**: 분석 기능 접근
- **viewer**: 조회 기능만 접근

## 📊 공통 응답 형식

### 성공 응답
```json
{
  "success": true,
  "data": {
    // 실제 데이터
  },
  "message": "요청이 성공적으로 처리되었습니다",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "uuid-here"
}
```

### 오류 응답
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력 데이터가 유효하지 않습니다",
    "details": {
      "field": "question",
      "reason": "질문이 비어있습니다"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "uuid-here"
}
```

### HTTP 상태 코드
- **200**: 성공
- **201**: 생성 성공
- **400**: 잘못된 요청
- **401**: 인증 실패
- **403**: 권한 없음
- **404**: 리소스 없음
- **408**: 요청 시간 초과
- **422**: 데이터 검증 실패
- **429**: 요청 한도 초과
- **500**: 서버 오류

## 🔑 인증 관리 API

### 1. 사용자 로그인

**POST** `/auth/login`

로그인하여 JWT 토큰을 발급받습니다.

#### 요청
```json
{
  "username": "user123",
  "password": "secure_password"
}
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 86400,
    "user": {
      "id": "uuid-here",
      "username": "user123",
      "full_name": "홍길동",
      "role": "user",
      "permissions": ["query:read", "excel:analyze"]
    }
  }
}
```

### 2. 토큰 갱신

**POST** `/auth/refresh`

기존 토큰을 갱신합니다.

#### 요청 헤더
```http
Authorization: Bearer <current_token>
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "access_token": "new_jwt_token_here",
    "expires_in": 86400
  }
}
```

### 3. 로그아웃

**POST** `/auth/logout`

현재 세션을 종료하고 토큰을 무효화합니다.

#### 응답 (200)
```json
{
  "success": true,
  "message": "성공적으로 로그아웃되었습니다"
}
```

## 🗄️ 데이터베이스 연결 관리 API

### 1. 연결 목록 조회

**GET** `/connections`

사용자가 접근 가능한 데이터베이스 연결 목록을 조회합니다.

#### 쿼리 파라미터
- `page`: 페이지 번호 (기본값: 1)
- `limit`: 페이지당 항목 수 (기본값: 20)
- `active_only`: 활성 연결만 조회 (기본값: true)

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "connections": [
      {
        "id": "uuid-here",
        "name": "main_db",
        "display_name": "메인 데이터베이스",
        "description": "고객 및 주문 데이터",
        "db_type": "postgresql",
        "is_active": true,
        "schema_info": {
          "tables_count": 25,
          "last_sync": "2024-01-15T09:00:00Z"
        },
        "permissions": {
          "can_query": true,
          "allowed_schemas": ["public"],
          "max_rows": 10000
        }
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 1,
      "has_next": false
    }
  }
}
```

### 2. 연결 상세 정보

**GET** `/connections/{connection_id}`

특정 데이터베이스 연결의 상세 정보를 조회합니다.

#### 경로 파라미터
- `connection_id`: 연결 ID (UUID)

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "name": "main_db",
    "display_name": "메인 데이터베이스",
    "description": "고객 및 주문 데이터",
    "db_type": "postgresql",
    "is_active": true,
    "schema_info": {
      "schemas": {
        "public": {
          "tables": {
            "customers": {
              "columns": [
                {"name": "id", "type": "integer", "nullable": false},
                {"name": "name", "type": "varchar", "nullable": false},
                {"name": "email", "type": "varchar", "nullable": true}
              ],
              "row_count": 1500
            },
            "orders": {
              "columns": [
                {"name": "id", "type": "integer", "nullable": false},
                {"name": "customer_id", "type": "integer", "nullable": false},
                {"name": "amount", "type": "decimal", "nullable": false},
                {"name": "order_date", "type": "timestamp", "nullable": false}
              ],
              "row_count": 5200
            }
          }
        }
      },
      "last_sync": "2024-01-15T09:00:00Z"
    }
  }
}
```

### 3. 스키마 정보 갱신

**POST** `/connections/{connection_id}/refresh-schema`

데이터베이스 스키마 정보를 다시 수집합니다.

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "updated_at": "2024-01-15T10:30:00Z",
    "tables_discovered": 25,
    "changes": {
      "new_tables": ["products_v2"],
      "removed_tables": [],
      "modified_tables": ["customers"]
    }
  }
}
```

## 🤖 자연어 분석 API

### 1. 질문 분석

**POST** `/analysis/analyze-question`

사용자의 자연어 질문을 분석하여 처리 유형을 결정합니다.

#### 요청
```json
{
  "question": "지난 달 매출 현황을 보여줘",
  "context": {
    "connection_id": "uuid-here",
    "previous_questions": [
      "고객 수는 몇 명이야?"
    ]
  }
}
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "analysis": {
      "type": "DB_QUERY",
      "intent": "매출 데이터 조회 및 시각화",
      "confidence": 0.95,
      "entities": {
        "time_period": "지난 달",
        "metric": "매출",
        "visualization": "현황"
      },
      "suggested_tables": ["orders", "products"],
      "complexity": "medium"
    },
    "suggestions": [
      "월별 매출 추이를 선 그래프로 보시겠습니까?",
      "제품별 매출 분석도 함께 확인해보세요"
    ]
  }
}
```

## 📊 데이터베이스 쿼리 API

### 1. SQL 쿼리 생성

**POST** `/query/generate-sql`

자연어 질문을 SQL 쿼리로 변환합니다.

#### 요청
```json
{
  "question": "지난 3개월 동안 월별 매출 합계",
  "connection_id": "uuid-here",
  "options": {
    "include_explanation": true,
    "optimize_for_visualization": true
  }
}
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "sql": "SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as total_sales FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY DATE_TRUNC('month', order_date) ORDER BY month",
    "explanation": "주문 테이블에서 최근 3개월간의 데이터를 월별로 그룹화하여 매출 합계를 계산합니다",
    "estimated_rows": 3,
    "tables_used": ["orders"],
    "complexity": "medium",
    "execution_plan": {
      "estimated_cost": 125.50,
      "estimated_time_ms": 45
    }
  }
}
```

### 2. SQL 쿼리 실행

**POST** `/query/execute`

생성된 SQL 쿼리를 실행하여 결과를 반환합니다.

#### 요청
```json
{
  "sql": "SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as total_sales FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY DATE_TRUNC('month', order_date) ORDER BY month",
  "connection_id": "uuid-here",
  "options": {
    "limit": 1000,
    "timeout": 30,
    "use_cache": true
  }
}
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "columns": [
      {"name": "month", "type": "timestamp"},
      {"name": "total_sales", "type": "numeric"}
    ],
    "rows": [
      {"month": "2023-11-01T00:00:00Z", "total_sales": 125000.50},
      {"month": "2023-12-01T00:00:00Z", "total_sales": 142300.75},
      {"month": "2024-01-01T00:00:00Z", "total_sales": 158750.25}
    ],
    "metadata": {
      "row_count": 3,
      "execution_time_ms": 42,
      "cache_hit": false,
      "data_types": {
        "month": "datetime",
        "total_sales": "currency"
      }
    }
  }
}
```

### 3. 통합 분석 실행

**POST** `/analysis/execute`

질문 분석부터 시각화까지 전체 프로세스를 한 번에 실행합니다.

#### 요청
```json
{
  "question": "지난 3개월 매출 추이를 보여줘",
  "connection_id": "uuid-here",
  "options": {
    "auto_visualize": true,
    "include_insights": true,
    "chart_type": "auto"
  }
}
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "analysis": {
      "question": "지난 3개월 매출 추이를 보여줘",
      "type": "DB_QUERY",
      "sql": "SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as total_sales FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY DATE_TRUNC('month', order_date) ORDER BY month"
    },
    "results": {
      "columns": ["month", "total_sales"],
      "rows": [
        {"month": "2023-11-01T00:00:00Z", "total_sales": 125000.50},
        {"month": "2023-12-01T00:00:00Z", "total_sales": 142300.75},
        {"month": "2024-01-01T00:00:00Z", "total_sales": 158750.25}
      ],
      "row_count": 3
    },
    "visualization": {
      "chart_type": "line",
      "config": {
        "x_axis": "month",
        "y_axis": "total_sales",
        "title": "월별 매출 추이",
        "color_scheme": "blue"
      },
      "chart_data": "base64_encoded_plotly_json",
      "chart_html": "<div>plotly chart html</div>"
    },
    "insights": {
      "summary": "최근 3개월간 매출이 지속적으로 증가하고 있습니다.",
      "key_findings": [
        "12월 매출이 11월 대비 13.8% 증가",
        "1월 매출이 12월 대비 11.6% 증가",
        "3개월 평균 증가율: 12.7%"
      ],
      "recommendations": [
        "현재 증가 추세를 유지하기 위한 마케팅 전략 강화",
        "2월 매출 목표를 175,000으로 설정 권장"
      ]
    },
    "execution_info": {
      "total_time_ms": 1250,
      "sql_time_ms": 42,
      "visualization_time_ms": 180,
      "llm_time_ms": 1028
    }
  }
}
```

## 📁 Excel 분석 API

### 1. 파일 업로드

**POST** `/excel/upload`

Excel 파일을 업로드하고 기본 분석을 수행합니다.

#### 요청 (multipart/form-data)
```
Content-Type: multipart/form-data

file: [Excel 파일]
options: {
  "auto_detect_headers": true,
  "sheet_name": "Sheet1",
  "max_rows": 100000
}
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "file_id": "uuid-here",
    "file_info": {
      "filename": "sales_data.xlsx",
      "size_bytes": 2048576,
      "sheet_count": 3,
      "active_sheet": "Sheet1"
    },
    "data_info": {
      "shape": [1500, 8],
      "columns": [
        {"name": "date", "type": "datetime", "null_count": 0},
        {"name": "product", "type": "string", "null_count": 5},
        {"name": "sales", "type": "float", "null_count": 2},
        {"name": "quantity", "type": "int", "null_count": 0}
      ],
      "memory_usage": "1.2MB"
    },
    "preview": [
      {"date": "2024-01-01", "product": "상품A", "sales": 1000.50, "quantity": 10},
      {"date": "2024-01-02", "product": "상품B", "sales": 1500.75, "quantity": 15}
    ],
    "basic_stats": {
      "sales": {
        "mean": 1250.30,
        "median": 1200.00,
        "std": 325.50,
        "min": 100.00,
        "max": 5000.00
      }
    }
  }
}
```

### 2. Excel 데이터 분석

**POST** `/excel/{file_id}/analyze`

업로드된 Excel 파일에 대해 자연어 질문으로 분석을 수행합니다.

#### 경로 파라미터
- `file_id`: 업로드된 파일 ID

#### 요청
```json
{
  "question": "월별 매출 합계를 계산해줘",
  "options": {
    "auto_visualize": true,
    "include_code": true
  }
}
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "analysis": {
      "question": "월별 매출 합계를 계산해줘",
      "generated_code": "monthly_sales = df.groupby(df['date'].dt.to_period('M'))['sales'].sum()\nresult = monthly_sales.reset_index()",
      "execution_success": true
    },
    "results": {
      "columns": ["date", "sales"],
      "rows": [
        {"date": "2024-01", "sales": 125000.50},
        {"date": "2024-02", "sales": 142300.75}
      ],
      "row_count": 2
    },
    "visualization": {
      "chart_type": "bar",
      "config": {
        "x_axis": "date",
        "y_axis": "sales",
        "title": "월별 매출 합계"
      },
      "chart_data": "base64_encoded_plotly_json"
    },
    "insights": {
      "summary": "2개월간 총 매출은 267,301원이며, 2월이 1월보다 13.8% 증가했습니다.",
      "trends": ["매출 증가 추세"]
    }
  }
}
```

### 3. 파일 목록 조회

**GET** `/excel/files`

현재 세션에서 업로드된 파일 목록을 조회합니다.

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "files": [
      {
        "file_id": "uuid-here",
        "filename": "sales_data.xlsx",
        "uploaded_at": "2024-01-15T10:00:00Z",
        "expires_at": "2024-01-15T14:00:00Z",
        "data_shape": [1500, 8],
        "analysis_count": 3
      }
    ]
  }
}
```

## 📈 시각화 API

### 1. 차트 생성

**POST** `/visualization/create-chart`

데이터를 기반으로 차트를 생성합니다.

#### 요청
```json
{
  "data": {
    "columns": ["month", "sales"],
    "rows": [
      {"month": "2024-01", "sales": 125000},
      {"month": "2024-02", "sales": 142300}
    ]
  },
  "chart_config": {
    "type": "line",
    "x_axis": "month",
    "y_axis": "sales",
    "title": "월별 매출 추이",
    "color_scheme": "blue",
    "interactive": true
  }
}
```

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "chart_id": "uuid-here",
    "chart_type": "line",
    "plotly_json": {
      "data": [...],
      "layout": {...},
      "config": {...}
    },
    "chart_html": "<div id='chart'>...</div>",
    "static_image": {
      "png": "base64_encoded_png",
      "svg": "base64_encoded_svg"
    },
    "download_urls": {
      "png": "/api/v1/visualization/uuid-here/download?format=png",
      "svg": "/api/v1/visualization/uuid-here/download?format=svg",
      "html": "/api/v1/visualization/uuid-here/download?format=html"
    }
  }
}
```

### 2. 차트 다운로드

**GET** `/visualization/{chart_id}/download`

생성된 차트를 다양한 형식으로 다운로드합니다.

#### 경로 파라미터
- `chart_id`: 차트 ID

#### 쿼리 파라미터
- `format`: 다운로드 형식 (png, svg, html, pdf)
- `width`: 이미지 너비 (기본값: 800)
- `height`: 이미지 높이 (기본값: 600)

#### 응답 (200)
```
Content-Type: image/png (또는 요청한 형식에 따라)
Content-Disposition: attachment; filename="chart.png"

[바이너리 데이터]
```

## 📚 질문 이력 API

### 1. 질문 이력 조회

**GET** `/history/questions`

사용자의 질문 이력을 조회합니다.

#### 쿼리 파라미터
- `page`: 페이지 번호 (기본값: 1)
- `limit`: 페이지당 항목 수 (기본값: 20)
- `type`: 질문 유형 필터 (database, excel, general)
- `date_from`: 시작 날짜 (ISO 8601)
- `date_to`: 종료 날짜 (ISO 8601)

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "questions": [
      {
        "id": "uuid-here",
        "question": "지난 달 매출 현황을 보여줘",
        "type": "database",
        "connection_name": "main_db",
        "status": "success",
        "created_at": "2024-01-15T10:30:00Z",
        "execution_time_ms": 1250,
        "result_summary": "3개월 매출 데이터, 선 그래프 생성"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "has_next": true
    }
  }
}
```

### 2. 질문 상세 조회

**GET** `/history/questions/{question_id}`

특정 질문의 상세 결과를 조회합니다.

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "question": "지난 달 매출 현황을 보여줘",
    "type": "database",
    "connection_id": "uuid-here",
    "sql": "SELECT ...",
    "results": {
      "columns": ["month", "sales"],
      "rows": [...],
      "row_count": 3
    },
    "visualization": {
      "chart_type": "line",
      "chart_html": "...",
      "download_urls": {...}
    },
    "insights": {
      "summary": "...",
      "key_findings": [...]
    },
    "created_at": "2024-01-15T10:30:00Z",
    "execution_time_ms": 1250
  }
}
```

### 3. 즐겨찾기 관리

**POST** `/history/questions/{question_id}/favorite`

질문을 즐겨찾기에 추가합니다.

#### 응답 (200)
```json
{
  "success": true,
  "message": "즐겨찾기에 추가되었습니다"
}
```

**DELETE** `/history/questions/{question_id}/favorite`

즐겨찾기에서 제거합니다.

## ⚙️ 시스템 관리 API

### 1. 시스템 상태 확인

**GET** `/health`

시스템 전반적인 상태를 확인합니다.

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "uptime_seconds": 86400,
    "services": {
      "database": {
        "status": "healthy",
        "response_time_ms": 15,
        "connections_active": 8,
        "connections_max": 20
      },
      "redis": {
        "status": "healthy",
        "response_time_ms": 2,
        "memory_usage": "45MB",
        "keys_count": 1250
      },
      "openai_api": {
        "status": "healthy",
        "response_time_ms": 850,
        "rate_limit_remaining": 9500
      }
    },
    "metrics": {
      "requests_total": 12450,
      "requests_per_minute": 125,
      "average_response_time_ms": 650,
      "error_rate": 0.02
    }
  }
}
```

### 2. 사용 통계 조회

**GET** `/admin/stats`

시스템 사용 통계를 조회합니다. (관리자 권한 필요)

#### 쿼리 파라미터
- `period`: 조회 기간 (day, week, month)
- `date_from`: 시작 날짜
- `date_to`: 종료 날짜

#### 응답 (200)
```json
{
  "success": true,
  "data": {
    "period": "week",
    "date_range": {
      "from": "2024-01-08T00:00:00Z",
      "to": "2024-01-15T00:00:00Z"
    },
    "usage_stats": {
      "total_users": 125,
      "active_users": 87,
      "total_questions": 2450,
      "successful_queries": 2301,
      "failed_queries": 149,
      "excel_analyses": 180
    },
    "performance_stats": {
      "avg_response_time_ms": 1250,
      "avg_sql_time_ms": 85,
      "avg_llm_time_ms": 950,
      "cache_hit_rate": 0.65
    },
    "popular_questions": [
      {
        "question": "월별 매출 현황",
        "count": 145,
        "avg_response_time_ms": 1100
      }
    ]
  }
}
```

## 🚨 오류 코드 정의

### 인증 관련 오류
- **AUTH_001**: 유효하지 않은 토큰
- **AUTH_002**: 토큰 만료
- **AUTH_003**: 권한 부족
- **AUTH_004**: 로그인 실패

### 요청 관련 오류
- **REQUEST_001**: 잘못된 요청 형식
- **REQUEST_002**: 필수 필드 누락
- **REQUEST_003**: 데이터 검증 실패
- **REQUEST_004**: 파일 형식 오류

### 데이터베이스 관련 오류
- **DB_001**: 연결 실패
- **DB_002**: SQL 구문 오류
- **DB_003**: 실행 시간 초과
- **DB_004**: 권한 부족

### 분석 관련 오류
- **ANALYSIS_001**: 질문 분석 실패
- **ANALYSIS_002**: SQL 생성 실패
- **ANALYSIS_003**: 코드 실행 실패
- **ANALYSIS_004**: 시각화 생성 실패

### 시스템 관련 오류
- **SYSTEM_001**: 서버 내부 오류
- **SYSTEM_002**: 서비스 일시 중단
- **SYSTEM_003**: 리소스 부족
- **SYSTEM_004**: 외부 API 오류

## 📋 Rate Limiting

### 제한 정책
- **일반 사용자**: 분당 100회, 시간당 1000회
- **관리자**: 분당 200회, 시간당 2000회
- **분석 요청**: 분당 20회 (LLM 비용 고려)

### Rate Limit 헤더
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995260
```

### 제한 초과시 응답 (429)
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "요청 한도를 초과했습니다",
    "details": {
      "limit": 100,
      "reset_at": "2024-01-15T10:31:00Z"
    }
  }
}
```

## 🔧 SDK 및 클라이언트 라이브러리

### Python SDK 예시

```python
from datagenie import DataGenieClient

# 클라이언트 초기화
client = DataGenieClient(
    api_key="your_api_key",
    base_url="https://api.datagenie.com/api/v1"
)

# 로그인
client.login("username", "password")

# 데이터베이스 질의
result = client.query.execute(
    question="지난 달 매출 현황을 보여줘",
    connection_id="uuid-here"
)

# Excel 분석
file_result = client.excel.upload("sales_data.xlsx")
analysis = client.excel.analyze(
    file_id=file_result.file_id,
    question="월별 매출 합계"
)

# 시각화
chart = client.visualization.create_chart(
    data=result.data,
    chart_type="line"
)
```

### JavaScript/TypeScript SDK 예시

```typescript
import { DataGenieClient } from '@datagenie/sdk';

const client = new DataGenieClient({
  apiKey: 'your_api_key',
  baseURL: 'https://api.datagenie.com/api/v1'
});

// 인증
await client.auth.login('username', 'password');

// 질의 실행
const result = await client.analysis.execute({
  question: '지난 달 매출 현황을 보여줘',
  connectionId: 'uuid-here',
  options: {
    autoVisualize: true,
    includeInsights: true
  }
});

console.log(result.data.insights);
```

## 📖 API 사용 예시

### 1. 완전한 분석 워크플로우

```bash
# 1. 로그인
curl -X POST "https://api.datagenie.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user123",
    "password": "password"
  }'

# 2. 연결 목록 조회
curl -X GET "https://api.datagenie.com/api/v1/connections" \
  -H "Authorization: Bearer <token>"

# 3. 통합 분석 실행
curl -X POST "https://api.datagenie.com/api/v1/analysis/execute" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "지난 3개월 매출 추이를 보여줘",
    "connection_id": "uuid-here",
    "options": {
      "auto_visualize": true,
      "include_insights": true
    }
  }'
```

### 2. Excel 파일 분석

```bash
# 1. 파일 업로드
curl -X POST "https://api.datagenie.com/api/v1/excel/upload" \
  -H "Authorization: Bearer <token>" \
  -F "file=@sales_data.xlsx" \
  -F 'options={"auto_detect_headers": true}'

# 2. 분석 실행
curl -X POST "https://api.datagenie.com/api/v1/excel/<file_id>/analyze" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "월별 매출 합계를 계산해줘",
    "options": {
      "auto_visualize": true,
      "include_code": true
    }
  }'
```

---

**문서 승인**: ✅ API 명세서 작성 완료  
**다음 단계**: UI/UX 설계서 작성
