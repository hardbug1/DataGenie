"""
JWT Token Management System

Clean Architecture: Application Core
JWT 토큰 생성, 검증, 관리를 담당하는 핵심 인증 컴포넌트
"""

import jwt
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import structlog
import os

logger = structlog.get_logger(__name__)


class TokenType(Enum):
    """토큰 유형"""
    ACCESS = "access"
    REFRESH = "refresh"


@dataclass(frozen=True)
class TokenPayload:
    """JWT 토큰 페이로드"""
    user_id: str
    username: str
    email: str
    role: str
    permissions: List[str]
    token_type: TokenType
    issued_at: datetime
    expires_at: datetime
    
    def is_expired(self) -> bool:
        """토큰 만료 여부 확인"""
        return datetime.now(timezone.utc) > self.expires_at
    
    def has_permission(self, permission: str) -> bool:
        """특정 권한 보유 여부 확인"""
        return permission in self.permissions
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "permissions": self.permissions,
            "token_type": self.token_type.value,
            "iat": int(self.issued_at.timestamp()),
            "exp": int(self.expires_at.timestamp())
        }


@dataclass(frozen=True)
class TokenValidationResult:
    """토큰 검증 결과"""
    is_valid: bool
    payload: Optional[TokenPayload]
    error_message: Optional[str] = None
    
    def is_success(self) -> bool:
        """검증 성공 여부"""
        return self.is_valid and self.payload is not None


class JWTManager:
    """
    JWT 토큰 관리자
    
    API Development 규칙 준수:
    - JWT 토큰 생성 및 검증
    - 보안 키 관리
    - 토큰 만료 처리
    """
    
    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7
    ):
        """
        JWT 관리자 초기화
        
        Args:
            secret_key: JWT 서명 키 (환경변수에서 가져옴)
            algorithm: JWT 알고리즘
            access_token_expire_minutes: 액세스 토큰 만료 시간 (분)
            refresh_token_expire_days: 리프레시 토큰 만료 시간 (일)
        """
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY")
        if not self.secret_key:
            raise ValueError("JWT_SECRET_KEY 환경변수가 설정되지 않았습니다")
        
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        
        # 토큰 블랙리스트 (실제로는 Redis 등 외부 저장소 사용)
        self._blacklisted_tokens = set()
    
    def create_access_token(
        self,
        user_id: str,
        username: str,
        email: str,
        role: str,
        permissions: List[str]
    ) -> str:
        """
        액세스 토큰 생성
        
        Args:
            user_id: 사용자 ID
            username: 사용자명
            email: 이메일
            role: 역할
            permissions: 권한 목록
            
        Returns:
            str: JWT 액세스 토큰
        """
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=self.access_token_expire_minutes)
        
        payload = TokenPayload(
            user_id=user_id,
            username=username,
            email=email,
            role=role,
            permissions=permissions,
            token_type=TokenType.ACCESS,
            issued_at=now,
            expires_at=expires_at
        )
        
        token = jwt.encode(
            payload.to_dict(),
            self.secret_key,
            algorithm=self.algorithm
        )
        
        logger.info(
            "액세스 토큰 생성",
            extra={
                "user_id": user_id,
                "username": username,
                "expires_at": expires_at.isoformat(),
                "permissions_count": len(permissions)
            }
        )
        
        return token
    
    def create_refresh_token(
        self,
        user_id: str,
        username: str,
        email: str,
        role: str
    ) -> str:
        """
        리프레시 토큰 생성
        
        Args:
            user_id: 사용자 ID
            username: 사용자명
            email: 이메일
            role: 역할
            
        Returns:
            str: JWT 리프레시 토큰
        """
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=self.refresh_token_expire_days)
        
        payload = TokenPayload(
            user_id=user_id,
            username=username,
            email=email,
            role=role,
            permissions=[],  # 리프레시 토큰은 권한 정보 없음
            token_type=TokenType.REFRESH,
            issued_at=now,
            expires_at=expires_at
        )
        
        token = jwt.encode(
            payload.to_dict(),
            self.secret_key,
            algorithm=self.algorithm
        )
        
        logger.info(
            "리프레시 토큰 생성",
            extra={
                "user_id": user_id,
                "username": username,
                "expires_at": expires_at.isoformat()
            }
        )
        
        return token
    
    def validate_token(self, token: str) -> TokenValidationResult:
        """
        토큰 검증
        
        Args:
            token: 검증할 JWT 토큰
            
        Returns:
            TokenValidationResult: 검증 결과
        """
        try:
            # 블랙리스트 확인
            if self._is_blacklisted(token):
                return TokenValidationResult(
                    is_valid=False,
                    payload=None,
                    error_message="토큰이 블랙리스트에 등록되어 있습니다"
                )
            
            # JWT 디코딩 및 검증
            decoded_payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            # 페이로드 파싱
            payload = self._parse_payload(decoded_payload)
            
            # 만료 시간 확인
            if payload.is_expired():
                return TokenValidationResult(
                    is_valid=False,
                    payload=None,
                    error_message="토큰이 만료되었습니다"
                )
            
            logger.debug(
                "토큰 검증 성공",
                extra={
                    "user_id": payload.user_id,
                    "token_type": payload.token_type.value,
                    "expires_at": payload.expires_at.isoformat()
                }
            )
            
            return TokenValidationResult(
                is_valid=True,
                payload=payload
            )
            
        except jwt.ExpiredSignatureError:
            return TokenValidationResult(
                is_valid=False,
                payload=None,
                error_message="토큰이 만료되었습니다"
            )
        except jwt.InvalidTokenError as e:
            logger.warning(
                "유효하지 않은 토큰",
                extra={"error": str(e)}
            )
            return TokenValidationResult(
                is_valid=False,
                payload=None,
                error_message="유효하지 않은 토큰입니다"
            )
        except Exception as e:
            logger.error(
                "토큰 검증 중 오류 발생",
                extra={"error": str(e)}
            )
            return TokenValidationResult(
                is_valid=False,
                payload=None,
                error_message="토큰 검증 중 오류가 발생했습니다"
            )
    
    def _parse_payload(self, decoded_payload: Dict[str, Any]) -> TokenPayload:
        """디코딩된 페이로드를 TokenPayload 객체로 변환"""
        return TokenPayload(
            user_id=decoded_payload["user_id"],
            username=decoded_payload["username"],
            email=decoded_payload["email"],
            role=decoded_payload["role"],
            permissions=decoded_payload.get("permissions", []),
            token_type=TokenType(decoded_payload["token_type"]),
            issued_at=datetime.fromtimestamp(decoded_payload["iat"], tz=timezone.utc),
            expires_at=datetime.fromtimestamp(decoded_payload["exp"], tz=timezone.utc)
        )
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        리프레시 토큰으로 새 액세스 토큰 생성
        
        Args:
            refresh_token: 리프레시 토큰
            
        Returns:
            Optional[str]: 새 액세스 토큰 (실패 시 None)
        """
        validation_result = self.validate_token(refresh_token)
        
        if not validation_result.is_valid or not validation_result.payload:
            return None
        
        payload = validation_result.payload
        
        # 리프레시 토큰인지 확인
        if payload.token_type != TokenType.REFRESH:
            logger.warning(
                "액세스 토큰으로 리프레시 시도",
                extra={"user_id": payload.user_id}
            )
            return None
        
        # TODO: 사용자 정보 및 권한을 데이터베이스에서 다시 조회
        # 현재는 기본 권한으로 설정
        permissions = ["analysis:execute", "query:read"]
        
        return self.create_access_token(
            user_id=payload.user_id,
            username=payload.username,
            email=payload.email,
            role=payload.role,
            permissions=permissions
        )
    
    def blacklist_token(self, token: str):
        """토큰을 블랙리스트에 추가 (로그아웃 시 사용)"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        self._blacklisted_tokens.add(token_hash)
        
        logger.info(
            "토큰 블랙리스트 추가",
            extra={"token_hash": token_hash[:16]}
        )
    
    def _is_blacklisted(self, token: str) -> bool:
        """토큰이 블랙리스트에 있는지 확인"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return token_hash in self._blacklisted_tokens
    
    def get_token_info(self, token: str) -> Optional[Dict[str, Any]]:
        """토큰 정보 조회 (디버깅용)"""
        validation_result = self.validate_token(token)
        
        if not validation_result.is_valid or not validation_result.payload:
            return None
        
        payload = validation_result.payload
        return {
            "user_id": payload.user_id,
            "username": payload.username,
            "role": payload.role,
            "token_type": payload.token_type.value,
            "issued_at": payload.issued_at.isoformat(),
            "expires_at": payload.expires_at.isoformat(),
            "is_expired": payload.is_expired(),
            "permissions": payload.permissions
        }


class AuthenticationError(Exception):
    """인증 관련 예외"""
    pass


class TokenExpiredError(AuthenticationError):
    """토큰 만료 예외"""
    pass


class InvalidTokenError(AuthenticationError):
    """유효하지 않은 토큰 예외"""
    pass
