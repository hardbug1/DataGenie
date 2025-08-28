#!/usr/bin/env python3
"""
Create Default Users Script

기본 사용자들을 데이터베이스에 생성하는 스크립트
"""

import asyncio
import sys
import os
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.models.user import User
from app.use_cases.auth.authenticate_user_use_case import AuthenticateUserUseCase
from app.infrastructure.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.config.database import init_database
import structlog

# 로깅 설정
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


async def create_default_users():
    """기본 사용자들 생성"""
    try:
        logger.info("기본 사용자 생성 시작")
        
        # 데이터베이스 초기화
        await init_database()
        
        # 사용자 저장소 생성
        user_repository = SQLAlchemyUserRepository()
        
        # 기본 사용자들 정의
        default_users = [
            {
                "id": "admin-user-id",
                "username": "admin",
                "email": "admin@datagenie.com",
                "full_name": "시스템 관리자",
                "password": "admin123",
                "role": "admin"
            },
            {
                "id": "user-user-id", 
                "username": "user",
                "email": "user@datagenie.com",
                "full_name": "일반 사용자",
                "password": "user123",
                "role": "user"
            },
            {
                "id": "analyst-user-id",
                "username": "analyst", 
                "email": "analyst@datagenie.com",
                "full_name": "데이터 분석가",
                "password": "analyst123",
                "role": "analyst"
            }
        ]
        
        created_count = 0
        
        for user_data in default_users:
            # 기존 사용자 확인
            existing_user = await user_repository.find_by_username(user_data["username"])
            
            if existing_user:
                logger.info(
                    "사용자가 이미 존재함",
                    username=user_data["username"]
                )
                continue
            
            # 새 사용자 생성
            user = User(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=AuthenticateUserUseCase.hash_password(user_data["password"]),
                role=user_data["role"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            await user_repository.save(user)
            created_count += 1
            
            logger.info(
                "사용자 생성됨",
                username=user_data["username"],
                role=user_data["role"]
            )
        
        logger.info(
            "기본 사용자 생성 완료",
            created_count=created_count,
            total_users=len(default_users)
        )
        
        # 생성된 사용자들 정보 출력
        print("\n=== 생성된 기본 사용자들 ===")
        for user_data in default_users:
            print(f"사용자명: {user_data['username']}")
            print(f"비밀번호: {user_data['password']}")
            print(f"역할: {user_data['role']}")
            print(f"이메일: {user_data['email']}")
            print("-" * 30)
        
        print("\n✅ 기본 사용자 생성이 완료되었습니다!")
        print("이제 위의 계정 정보로 로그인할 수 있습니다.")
        
    except Exception as e:
        logger.error("기본 사용자 생성 실패", error=str(e), exc_info=True)
        print(f"❌ 오류 발생: {str(e)}")
        sys.exit(1)


async def list_users():
    """현재 사용자 목록 조회"""
    try:
        logger.info("사용자 목록 조회 시작")
        
        user_repository = SQLAlchemyUserRepository()
        users = await user_repository.find_all(limit=100, active_only=False)
        
        print(f"\n=== 현재 등록된 사용자들 ({len(users)}명) ===")
        
        for user in users:
            status = "활성" if user.is_active else "비활성"
            print(f"ID: {user.id}")
            print(f"사용자명: {user.username}")
            print(f"이메일: {user.email}")
            print(f"역할: {user.role}")
            print(f"상태: {status}")
            print(f"생성일: {user.created_at}")
            if user.last_login_at:
                print(f"마지막 로그인: {user.last_login_at}")
            print("-" * 50)
        
    except Exception as e:
        logger.error("사용자 목록 조회 실패", error=str(e), exc_info=True)
        print(f"❌ 오류 발생: {str(e)}")


def print_usage():
    """사용법 출력"""
    print("사용법:")
    print("  python scripts/create_users.py create  # 기본 사용자들 생성")
    print("  python scripts/create_users.py list    # 현재 사용자 목록 조회")


async def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "create":
        await create_default_users()
    elif command == "list":
        await list_users()
    else:
        print(f"알 수 없는 명령어: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
