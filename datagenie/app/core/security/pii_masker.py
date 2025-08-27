"""
Personal Information Masking System

Clean Architecture: Application Core
개인정보 자동 탐지 및 마스킹을 담당하는 핵심 보안 컴포넌트
"""

import re
import hashlib
from typing import Any, Dict, List, Optional, Union, Pattern
from dataclasses import dataclass
from enum import Enum
import structlog

logger = structlog.get_logger(__name__)


class PIIType(Enum):
    """개인정보 유형"""
    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"  # 주민등록번호
    CREDIT_CARD = "credit_card"
    KOREAN_RRN = "korean_rrn"  # 한국 주민등록번호
    IP_ADDRESS = "ip_address"
    PASSPORT = "passport"
    BANK_ACCOUNT = "bank_account"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PIIDetectionResult:
    """개인정보 탐지 결과"""
    pii_type: PIIType
    original_value: str
    masked_value: str
    confidence: float
    position: Optional[int] = None


@dataclass(frozen=True)
class MaskingResult:
    """마스킹 결과"""
    original_data: Any
    masked_data: Any
    detected_pii: List[PIIDetectionResult]
    masking_applied: bool
    
    def has_pii(self) -> bool:
        """개인정보가 탐지되었는지 확인"""
        return len(self.detected_pii) > 0


class PIIMasker:
    """
    개인정보 마스킹 시스템
    
    Database Security 규칙 준수:
    - 자동 PII 탐지
    - 다양한 개인정보 유형 지원
    - 안전한 마스킹 처리
    """
    
    # 개인정보 패턴 정의 (Database Security 규칙)
    PII_PATTERNS = {
        PIIType.EMAIL: {
            'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'confidence': 0.95
        },
        PIIType.PHONE: {
            'pattern': r'\b(?:\+82|0)(?:10|11|16|17|18|19)-?\d{3,4}-?\d{4}\b',
            'confidence': 0.90
        },
        PIIType.KOREAN_RRN: {
            'pattern': r'\b\d{6}-[1-4]\d{6}\b',
            'confidence': 0.98
        },
        PIIType.SSN: {
            'pattern': r'\b\d{3}-\d{2}-\d{4}\b',
            'confidence': 0.85
        },
        PIIType.CREDIT_CARD: {
            'pattern': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'confidence': 0.80
        },
        PIIType.IP_ADDRESS: {
            'pattern': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'confidence': 0.70
        },
        PIIType.PASSPORT: {
            'pattern': r'\b[A-Z]{1,2}\d{7,9}\b',
            'confidence': 0.75
        },
        PIIType.BANK_ACCOUNT: {
            'pattern': r'\b\d{10,16}\b',
            'confidence': 0.60
        }
    }
    
    def __init__(self, min_confidence: float = 0.7):
        """
        PII 마스킹 시스템 초기화
        
        Args:
            min_confidence: 최소 신뢰도 임계값
        """
        self.min_confidence = min_confidence
        self._compiled_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[PIIType, Pattern]:
        """정규식 패턴 컴파일"""
        compiled = {}
        for pii_type, config in self.PII_PATTERNS.items():
            try:
                compiled[pii_type] = re.compile(config['pattern'], re.IGNORECASE)
            except re.error as e:
                logger.error(f"PII 패턴 컴파일 실패: {pii_type}", error=str(e))
        return compiled
    
    def mask_data(self, data: Any, context: Optional[Dict[str, Any]] = None) -> MaskingResult:
        """
        데이터에서 개인정보 탐지 및 마스킹
        
        Args:
            data: 마스킹할 데이터 (문자열, 딕셔너리, 리스트 등)
            context: 추가 컨텍스트 정보
            
        Returns:
            MaskingResult: 마스킹 결과
        """
        detected_pii = []
        masked_data = self._mask_recursive(data, detected_pii)
        
        # 마스킹 이벤트 로깅
        self._log_masking_event(detected_pii, context)
        
        return MaskingResult(
            original_data=data,
            masked_data=masked_data,
            detected_pii=detected_pii,
            masking_applied=len(detected_pii) > 0
        )
    
    def _mask_recursive(self, data: Any, detected_pii: List[PIIDetectionResult]) -> Any:
        """재귀적으로 데이터 구조를 탐색하며 마스킹"""
        if isinstance(data, str):
            return self._mask_string(data, detected_pii)
        elif isinstance(data, dict):
            return {key: self._mask_recursive(value, detected_pii) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._mask_recursive(item, detected_pii) for item in data]
        elif isinstance(data, tuple):
            return tuple(self._mask_recursive(item, detected_pii) for item in data)
        else:
            return data
    
    def _mask_string(self, text: str, detected_pii: List[PIIDetectionResult]) -> str:
        """문자열에서 PII 탐지 및 마스킹"""
        if not text or not isinstance(text, str):
            return text
        
        masked_text = text
        
        for pii_type, pattern in self._compiled_patterns.items():
            config = self.PII_PATTERNS[pii_type]
            
            # 신뢰도 확인
            if config['confidence'] < self.min_confidence:
                continue
            
            matches = list(pattern.finditer(masked_text))
            
            # 뒤에서부터 처리하여 인덱스 변화 방지
            for match in reversed(matches):
                original_value = match.group()
                masked_value = self._generate_mask(original_value, pii_type)
                
                # 탐지 결과 기록
                detected_pii.append(PIIDetectionResult(
                    pii_type=pii_type,
                    original_value=original_value,
                    masked_value=masked_value,
                    confidence=config['confidence'],
                    position=match.start()
                ))
                
                # 마스킹 적용
                masked_text = (
                    masked_text[:match.start()] + 
                    masked_value + 
                    masked_text[match.end():]
                )
        
        return masked_text
    
    def _generate_mask(self, value: str, pii_type: PIIType) -> str:
        """PII 유형에 따른 마스킹 생성"""
        if pii_type == PIIType.EMAIL:
            return self._mask_email(value)
        elif pii_type == PIIType.PHONE:
            return self._mask_phone(value)
        elif pii_type == PIIType.KOREAN_RRN:
            return self._mask_korean_rrn(value)
        elif pii_type == PIIType.SSN:
            return self._mask_ssn(value)
        elif pii_type == PIIType.CREDIT_CARD:
            return self._mask_credit_card(value)
        elif pii_type == PIIType.IP_ADDRESS:
            return self._mask_ip_address(value)
        elif pii_type == PIIType.PASSPORT:
            return self._mask_passport(value)
        elif pii_type == PIIType.BANK_ACCOUNT:
            return self._mask_bank_account(value)
        else:
            return self._mask_generic(value)
    
    def _mask_email(self, email: str) -> str:
        """이메일 마스킹: user@domain.com -> u***@domain.com"""
        if '@' not in email:
            return '***MASKED_EMAIL***'
        
        local, domain = email.split('@', 1)
        if len(local) <= 2:
            masked_local = '*' * len(local)
        else:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
        
        return f"{masked_local}@{domain}"
    
    def _mask_phone(self, phone: str) -> str:
        """전화번호 마스킹: 010-1234-5678 -> 010-****-5678"""
        # 숫자만 추출
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 8:
            return f"{digits[:3]}-****-{digits[-4:]}"
        return '***MASKED_PHONE***'
    
    def _mask_korean_rrn(self, rrn: str) -> str:
        """주민등록번호 마스킹: 123456-1234567 -> 123456-1******"""
        if '-' in rrn:
            front, back = rrn.split('-', 1)
            return f"{front}-{back[0]}{'*' * (len(back) - 1)}"
        return '***MASKED_RRN***'
    
    def _mask_ssn(self, ssn: str) -> str:
        """SSN 마스킹: 123-45-6789 -> ***-**-6789"""
        parts = ssn.split('-')
        if len(parts) == 3:
            return f"***-**-{parts[2]}"
        return '***MASKED_SSN***'
    
    def _mask_credit_card(self, card: str) -> str:
        """신용카드 마스킹: 1234-5678-9012-3456 -> ****-****-****-3456"""
        # 숫자만 추출
        digits = re.sub(r'\D', '', card)
        if len(digits) >= 12:
            return f"****-****-****-{digits[-4:]}"
        return '***MASKED_CARD***'
    
    def _mask_ip_address(self, ip: str) -> str:
        """IP 주소 마스킹: 192.168.1.100 -> 192.168.*.***"""
        parts = ip.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.*.***"
        return '***MASKED_IP***'
    
    def _mask_passport(self, passport: str) -> str:
        """여권번호 마스킹: M12345678 -> M*****678"""
        if len(passport) >= 6:
            return passport[0] + '*' * (len(passport) - 4) + passport[-3:]
        return '***MASKED_PASSPORT***'
    
    def _mask_bank_account(self, account: str) -> str:
        """계좌번호 마스킹: 1234567890123 -> 123****90123"""
        if len(account) >= 8:
            return account[:3] + '*' * (len(account) - 6) + account[-3:]
        return '***MASKED_ACCOUNT***'
    
    def _mask_generic(self, value: str) -> str:
        """일반적인 마스킹"""
        if len(value) <= 4:
            return '*' * len(value)
        return value[:2] + '*' * (len(value) - 4) + value[-2:]
    
    def _log_masking_event(self, detected_pii: List[PIIDetectionResult], context: Optional[Dict[str, Any]]):
        """마스킹 이벤트 로깅"""
        if not detected_pii:
            return
        
        pii_summary = {}
        for pii in detected_pii:
            pii_type = pii.pii_type.value
            if pii_type not in pii_summary:
                pii_summary[pii_type] = 0
            pii_summary[pii_type] += 1
        
        logger.info(
            "개인정보 마스킹 적용",
            extra={
                "pii_detected": pii_summary,
                "total_pii_count": len(detected_pii),
                "user_id": context.get("user_id") if context else None,
                "query_id": context.get("query_id") if context else None
            }
        )
    
    def detect_pii_types(self, text: str) -> List[PIIType]:
        """텍스트에서 PII 유형 탐지 (마스킹 없이)"""
        detected_types = []
        
        for pii_type, pattern in self._compiled_patterns.items():
            config = self.PII_PATTERNS[pii_type]
            
            if config['confidence'] >= self.min_confidence and pattern.search(text):
                detected_types.append(pii_type)
        
        return detected_types
    
    def is_sensitive_data(self, data: Any) -> bool:
        """데이터에 민감한 정보가 포함되어 있는지 확인"""
        if isinstance(data, str):
            return len(self.detect_pii_types(data)) > 0
        elif isinstance(data, (dict, list, tuple)):
            result = self.mask_data(data)
            return result.has_pii()
        return False


class PIIMaskingError(Exception):
    """PII 마스킹 관련 예외"""
    pass
