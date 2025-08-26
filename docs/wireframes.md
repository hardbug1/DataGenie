# DataGenie 와이어프레임

## 📋 문서 정보
- **프로젝트명**: DataGenie (LLM 기반 데이터 질의·분석·시각화 서비스)
- **작성일**: 2024년
- **버전**: 1.0

## 🖥️ 데스크톱 메인 화면

<svg width="1200" height="800" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
  <!-- 전체 배경 -->
  <rect width="1200" height="800" fill="#f9fafb"/>
  
  <!-- 헤더 -->
  <rect width="1200" height="60" fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>
  
  <!-- 로고 및 타이틀 -->
  <text x="24" y="35" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#2563eb">🧞‍♂️ DataGenie</text>
  <text x="150" y="35" font-family="Arial, sans-serif" font-size="12" fill="#6b7280">AI 데이터 분석 비서</text>
  
  <!-- 헤더 우측 버튼들 -->
  <rect x="1000" y="20" width="80" height="20" rx="10" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="1010" y="32" font-family="Arial, sans-serif" font-size="10" fill="#374151">👤 홍길동님</text>
  <circle cx="1110" cy="30" r="15" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="1105" y="34" font-family="Arial, sans-serif" font-size="12">⚙️</text>
  <rect x="1140" y="22" width="40" height="16" rx="8" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="1145" y="32" font-family="Arial, sans-serif" font-size="8" fill="#374151">로그아웃</text>
  
  <!-- 사이드바 -->
  <rect x="0" y="60" width="300" height="740" fill="#f9fafb" stroke="#e5e7eb" stroke-width="1"/>
  
  <!-- 사이드바 - 최근 질문 -->
  <text x="20" y="90" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#374151">📜 최근 질문</text>
  
  <!-- 질문 이력 아이템들 -->
  <rect x="20" y="100" width="260" height="40" rx="8" fill="#ffffff" stroke="#e5e7eb"/>
  <text x="30" y="115" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#111827">지난 3개월 매출 현황을 보여줘</text>
  <text x="30" y="128" font-family="Arial, sans-serif" font-size="8" fill="#6b7280">2024-01-15</text>
  <text x="240" y="128" font-family="Arial, sans-serif" font-size="8" fill="#6b7280">성공</text>
  
  <rect x="20" y="145" width="260" height="40" rx="8" fill="#ffffff" stroke="#e5e7eb"/>
  <text x="30" y="160" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#111827">월별 고객 증가율 분석</text>
  <text x="30" y="173" font-family="Arial, sans-serif" font-size="8" fill="#6b7280">2024-01-14</text>
  <text x="240" y="173" font-family="Arial, sans-serif" font-size="8" fill="#6b7280">성공</text>
  
  <rect x="20" y="190" width="260" height="40" rx="8" fill="#ffffff" stroke="#e5e7eb"/>
  <text x="30" y="205" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#111827">제품별 매출 순위</text>
  <text x="30" y="218" font-family="Arial, sans-serif" font-size="8" fill="#6b7280">2024-01-14</text>
  <text x="240" y="218" font-family="Arial, sans-serif" font-size="8" fill="#6b7280">성공</text>
  
  <!-- 사이드바 - 즐겨찾기 -->
  <line x1="20" y1="250" x2="280" y2="250" stroke="#e5e7eb"/>
  <text x="20" y="275" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#374151">⭐ 즐겨찾기</text>
  
  <rect x="20" y="285" width="260" height="30" rx="8" fill="#ffffff" stroke="#e5e7eb"/>
  <text x="30" y="303" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#111827">월별 매출 대시보드</text>
  
  <!-- 사이드바 - 빠른 설정 -->
  <line x1="20" y1="330" x2="280" y2="330" stroke="#e5e7eb"/>
  <text x="20" y="355" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#374151">⚙️ 빠른 설정</text>
  
  <rect x="20" y="365" width="12" height="12" rx="2" fill="#2563eb"/>
  <text x="40" y="375" font-family="Arial, sans-serif" font-size="10" fill="#374151">자동 시각화</text>
  
  <rect x="20" y="385" width="260" height="20" rx="4" fill="#ffffff" stroke="#d1d5db"/>
  <text x="25" y="397" font-family="Arial, sans-serif" font-size="9" fill="#6b7280">기본 차트 유형: 자동 선택</text>
  
  <!-- 메인 컨텐츠 영역 -->
  <rect x="300" y="60" width="900" height="740" fill="#ffffff"/>
  
  <!-- 환영 메시지 -->
  <text x="650" y="150" font-family="Arial, sans-serif" font-size="28" font-weight="bold" fill="#111827" text-anchor="middle">무엇을 알고 싶으신가요?</text>
  <text x="650" y="180" font-family="Arial, sans-serif" font-size="16" fill="#6b7280" text-anchor="middle">자연어로 질문하시면 데이터를 분석해드립니다.</text>
  
  <!-- 질문 입력 박스 -->
  <rect x="400" y="220" width="500" height="80" rx="16" fill="#ffffff" stroke="#d1d5db" stroke-width="2"/>
  <text x="420" y="245" font-family="Arial, sans-serif" font-size="14" fill="#9ca3af">예: 지난 3개월 매출 현황을 보여주세요</text>
  
  <!-- 분석 시작 버튼 -->
  <rect x="920" y="230" width="100" height="60" rx="12" fill="#2563eb"/>
  <text x="970" y="265" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">분석 시작</text>
  
  <!-- 예시 질문 버튼들 -->
  <rect x="450" y="330" width="100" height="30" rx="15" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="500" y="348" font-family="Arial, sans-serif" font-size="10" fill="#374151" text-anchor="middle">📊 월별 매출 추이</text>
  
  <rect x="570" y="330" width="100" height="30" rx="15" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="620" y="348" font-family="Arial, sans-serif" font-size="10" fill="#374151" text-anchor="middle">👥 신규 고객 분석</text>
  
  <rect x="690" y="330" width="100" height="30" rx="15" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="740" y="348" font-family="Arial, sans-serif" font-size="10" fill="#374151" text-anchor="middle">📈 제품별 성장률</text>
  
  <rect x="810" y="330" width="100" height="30" rx="15" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="860" y="348" font-family="Arial, sans-serif" font-size="10" fill="#374151" text-anchor="middle">🎯 목표 달성률</text>
  
  <!-- 데이터 소스 선택 영역 -->
  <rect x="350" y="390" width="600" height="120" rx="16" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="370" y="415" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#374151">📊 데이터 소스 선택</text>
  
  <!-- 탭 네비게이션 -->
  <rect x="370" y="425" width="80" height="25" fill="#2563eb"/>
  <text x="410" y="440" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#ffffff" text-anchor="middle">데이터베이스</text>
  
  <rect x="450" y="425" width="80" height="25" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="490" y="440" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#6b7280" text-anchor="middle">Excel 파일</text>
  
  <!-- 데이터베이스 선택 드롭다운 -->
  <rect x="370" y="460" width="200" height="30" rx="6" fill="#ffffff" stroke="#d1d5db"/>
  <text x="380" y="478" font-family="Arial, sans-serif" font-size="10" fill="#6b7280">연결할 데이터베이스 선택</text>
  <polygon points="560,470 570,480 560,490" fill="#6b7280"/>
  
  <!-- 푸터 -->
  <rect x="0" y="760" width="1200" height="40" fill="#f9fafb" stroke="#e5e7eb" stroke-width="1"/>
  <text x="600" y="782" font-family="Arial, sans-serif" font-size="10" fill="#9ca3af" text-anchor="middle">© 2024 DataGenie. All rights reserved.</text>
</svg>

## 📱 모바일 화면

<svg width="375" height="667" viewBox="0 0 375 667" xmlns="http://www.w3.org/2000/svg">
  <!-- 전체 배경 -->
  <rect width="375" height="667" fill="#f9fafb"/>
  
  <!-- 헤더 -->
  <rect width="375" height="60" fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>
  
  <!-- 햄버거 메뉴 -->
  <rect x="20" y="25" width="20" height="2" fill="#374151"/>
  <rect x="20" y="29" width="20" height="2" fill="#374151"/>
  <rect x="20" y="33" width="20" height="2" fill="#374151"/>
  
  <!-- 로고 -->
  <text x="60" y="38" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#2563eb">🧞‍♂️ DataGenie</text>
  
  <!-- 사용자 아이콘 -->
  <circle cx="330" cy="30" r="12" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="327" y="34" font-family="Arial, sans-serif" font-size="10">👤</text>
  
  <!-- 메인 컨텐츠 -->
  <rect x="20" y="80" width="335" height="567" fill="#ffffff" rx="12"/>
  
  <!-- 환영 메시지 -->
  <text x="187" y="130" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#111827" text-anchor="middle">무엇을 알고 싶으신가요?</text>
  <text x="187" y="155" font-family="Arial, sans-serif" font-size="12" fill="#6b7280" text-anchor="middle">자연어로 질문하시면 데이터를 분석해드립니다.</text>
  
  <!-- 질문 입력 박스 -->
  <rect x="40" y="180" width="295" height="60" rx="12" fill="#ffffff" stroke="#d1d5db" stroke-width="2"/>
  <text x="50" y="200" font-family="Arial, sans-serif" font-size="12" fill="#9ca3af">예: 지난 3개월 매출 현황을</text>
  <text x="50" y="215" font-family="Arial, sans-serif" font-size="12" fill="#9ca3af">보여주세요</text>
  
  <!-- 분석 시작 버튼 -->
  <rect x="40" y="255" width="295" height="40" rx="20" fill="#2563eb"/>
  <text x="187" y="278" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">분석 시작</text>
  
  <!-- 예시 질문 버튼들 (세로 배열) -->
  <rect x="40" y="315" width="295" height="35" rx="17" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="187" y="336" font-family="Arial, sans-serif" font-size="12" fill="#374151" text-anchor="middle">📊 월별 매출 추이</text>
  
  <rect x="40" y="360" width="295" height="35" rx="17" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="187" y="381" font-family="Arial, sans-serif" font-size="12" fill="#374151" text-anchor="middle">👥 신규 고객 분석</text>
  
  <rect x="40" y="405" width="295" height="35" rx="17" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="187" y="426" font-family="Arial, sans-serif" font-size="12" fill="#374151" text-anchor="middle">📈 제품별 성장률</text>
  
  <rect x="40" y="450" width="295" height="35" rx="17" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="187" y="471" font-family="Arial, sans-serif" font-size="12" fill="#374151" text-anchor="middle">🎯 목표 달성률</text>
  
  <!-- 데이터 소스 선택 -->
  <rect x="40" y="505" width="295" height="100" rx="12" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="50" y="525" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#374151">📊 데이터 소스 선택</text>
  
  <!-- 탭 (모바일용) -->
  <rect x="50" y="535" width="80" height="25" fill="#2563eb"/>
  <text x="90" y="550" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#ffffff" text-anchor="middle">데이터베이스</text>
  
  <rect x="135" y="535" width="80" height="25" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="175" y="550" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#6b7280" text-anchor="middle">Excel</text>
  
  <!-- 드롭다운 -->
  <rect x="50" y="570" width="225" height="25" rx="4" fill="#ffffff" stroke="#d1d5db"/>
  <text x="60" y="585" font-family="Arial, sans-serif" font-size="10" fill="#6b7280">데이터베이스 선택</text>
</svg>

## 📊 분석 결과 화면 (데스크톱)

<svg width="1200" height="800" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
  <!-- 전체 배경 -->
  <rect width="1200" height="800" fill="#f9fafb"/>
  
  <!-- 헤더 (동일) -->
  <rect width="1200" height="60" fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>
  <text x="24" y="35" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#2563eb">🧞‍♂️ DataGenie</text>
  <text x="150" y="35" font-family="Arial, sans-serif" font-size="12" fill="#6b7280">AI 데이터 분석 비서</text>
  
  <!-- 사이드바 (축소) -->
  <rect x="0" y="60" width="300" height="740" fill="#f9fafb" stroke="#e5e7eb" stroke-width="1"/>
  
  <!-- 메인 컨텐츠 영역 -->
  <rect x="300" y="60" width="900" height="740" fill="#ffffff"/>
  
  <!-- 결과 헤더 -->
  <text x="330" y="90" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#111827">📊 분석 결과</text>
  
  <!-- 액션 버튼들 -->
  <rect x="1050" y="70" width="60" height="25" rx="12" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="1080" y="85" font-family="Arial, sans-serif" font-size="9" fill="#374151" text-anchor="middle">📥 내보내기</text>
  
  <rect x="1120" y="70" width="40" height="25" rx="12" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="1140" y="85" font-family="Arial, sans-serif" font-size="9" fill="#374151" text-anchor="middle">🔗 공유</text>
  
  <rect x="1170" y="70" width="20" height="25" rx="12" fill="#f59e0b"/>
  <text x="1180" y="85" font-family="Arial, sans-serif" font-size="9" fill="#ffffff" text-anchor="middle">⭐</text>
  
  <!-- 인사이트 카드 -->
  <rect x="330" y="110" width="840" height="80" rx="12" fill="url(#gradient1)"/>
  <defs>
    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
    </linearGradient>
  </defs>
  <text x="350" y="135" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#ffffff">💡 주요 인사이트</text>
  <text x="350" y="155" font-family="Arial, sans-serif" font-size="12" fill="#ffffff">• 최근 3개월간 매출이 지속적으로 증가하고 있습니다 (평균 12.7% 증가)</text>
  <text x="350" y="170" font-family="Arial, sans-serif" font-size="12" fill="#ffffff">• 1월 매출이 158,750원으로 최고치를 기록했습니다</text>
  
  <!-- 탭 네비게이션 -->
  <rect x="330" y="210" width="60" height="30" fill="#2563eb"/>
  <text x="360" y="228" font-family="Arial, sans-serif" font-size="11" font-weight="500" fill="#ffffff" text-anchor="middle">📈 차트</text>
  
  <rect x="390" y="210" width="60" height="30" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="420" y="228" font-family="Arial, sans-serif" font-size="11" font-weight="500" fill="#6b7280" text-anchor="middle">📋 데이터</text>
  
  <rect x="450" y="210" width="60" height="30" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="480" y="228" font-family="Arial, sans-serif" font-size="11" font-weight="500" fill="#6b7280" text-anchor="middle">💻 코드</text>
  
  <!-- 차트 영역 -->
  <rect x="330" y="250" width="840" height="400" rx="8" fill="#ffffff" stroke="#e5e7eb"/>
  
  <!-- 모의 선 그래프 -->
  <text x="350" y="275" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#111827">월별 매출 추이</text>
  
  <!-- Y축 -->
  <line x1="370" y1="300" x2="370" y2="620" stroke="#d1d5db" stroke-width="2"/>
  <text x="365" y="305" font-family="Arial, sans-serif" font-size="10" fill="#6b7280" text-anchor="end">160K</text>
  <text x="365" y="380" font-family="Arial, sans-serif" font-size="10" fill="#6b7280" text-anchor="end">140K</text>
  <text x="365" y="455" font-family="Arial, sans-serif" font-size="10" fill="#6b7280" text-anchor="end">120K</text>
  <text x="365" y="530" font-family="Arial, sans-serif" font-size="10" fill="#6b7280" text-anchor="end">100K</text>
  <text x="365" y="605" font-family="Arial, sans-serif" font-size="10" fill="#6b7280" text-anchor="end">80K</text>
  
  <!-- X축 -->
  <line x1="370" y1="620" x2="1140" y2="620" stroke="#d1d5db" stroke-width="2"/>
  <text x="570" y="635" font-family="Arial, sans-serif" font-size="10" fill="#6b7280" text-anchor="middle">11월</text>
  <text x="755" y="635" font-family="Arial, sans-serif" font-size="10" fill="#6b7280" text-anchor="middle">12월</text>
  <text x="940" y="635" font-family="Arial, sans-serif" font-size="10" fill="#6b7280" text-anchor="middle">1월</text>
  
  <!-- 데이터 포인트와 선 -->
  <circle cx="570" cy="530" r="4" fill="#2563eb"/>
  <circle cx="755" cy="455" r="4" fill="#2563eb"/>
  <circle cx="940" cy="380" r="4" fill="#2563eb"/>
  
  <polyline points="570,530 755,455 940,380" fill="none" stroke="#2563eb" stroke-width="3"/>
  
  <!-- 데이터 레이블 -->
  <text x="570" y="520" font-family="Arial, sans-serif" font-size="9" fill="#111827" text-anchor="middle">125,000</text>
  <text x="755" y="445" font-family="Arial, sans-serif" font-size="9" fill="#111827" text-anchor="middle">142,300</text>
  <text x="940" y="370" font-family="Arial, sans-serif" font-size="9" fill="#111827" text-anchor="middle">158,750</text>
  
  <!-- 차트 컨트롤 -->
  <rect x="500" y="660" width="300" height="40" rx="8" fill="#f9fafb"/>
  <rect x="520" y="670" width="50" height="20" rx="4" fill="#2563eb"/>
  <text x="545" y="682" font-family="Arial, sans-serif" font-size="8" fill="#ffffff" text-anchor="middle">PNG 다운로드</text>
  
  <rect x="580" y="670" width="50" height="20" rx="4" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="605" y="682" font-family="Arial, sans-serif" font-size="8" fill="#374151" text-anchor="middle">SVG 다운로드</text>
  
  <rect x="640" y="670" width="50" height="20" rx="4" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="665" y="682" font-family="Arial, sans-serif" font-size="8" fill="#374151" text-anchor="middle">확대/축소</text>
  
  <rect x="700" y="670" width="50" height="20" rx="4" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="725" y="682" font-family="Arial, sans-serif" font-size="8" fill="#374151" text-anchor="middle">전체화면</text>
</svg>

## 📱 분석 결과 화면 (모바일)

<svg width="375" height="667" viewBox="0 0 375 667" xmlns="http://www.w3.org/2000/svg">
  <!-- 전체 배경 -->
  <rect width="375" height="667" fill="#f9fafb"/>
  
  <!-- 헤더 -->
  <rect width="375" height="60" fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>
  <text x="20" y="38" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#2563eb">← 분석 결과</text>
  
  <!-- 메인 컨텐츠 -->
  <rect x="20" y="80" width="335" height="567" fill="#ffffff" rx="12"/>
  
  <!-- 인사이트 카드 -->
  <rect x="40" y="100" width="295" height="70" rx="8" fill="url(#gradient2)"/>
  <defs>
    <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
    </linearGradient>
  </defs>
  <text x="50" y="120" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#ffffff">💡 주요 인사이트</text>
  <text x="50" y="135" font-family="Arial, sans-serif" font-size="10" fill="#ffffff">• 최근 3개월간 매출 12.7% 증가</text>
  <text x="50" y="148" font-family="Arial, sans-serif" font-size="10" fill="#ffffff">• 1월 매출 최고치 달성 (158,750원)</text>
  <text x="50" y="161" font-family="Arial, sans-serif" font-size="10" fill="#ffffff">• 지속적인 상승 추세</text>
  
  <!-- 탭 네비게이션 -->
  <rect x="40" y="185" width="70" height="25" fill="#2563eb"/>
  <text x="75" y="200" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#ffffff" text-anchor="middle">📈 차트</text>
  
  <rect x="115" y="185" width="70" height="25" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="150" y="200" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#6b7280" text-anchor="middle">📋 데이터</text>
  
  <rect x="190" y="185" width="70" height="25" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="225" y="200" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#6b7280" text-anchor="middle">💻 코드</text>
  
  <!-- 액션 버튼 -->
  <circle cx="315" cy="197" r="12" fill="#f59e0b"/>
  <text x="315" y="201" font-family="Arial, sans-serif" font-size="8" fill="#ffffff" text-anchor="middle">⭐</text>
  
  <!-- 차트 영역 -->
  <rect x="40" y="225" width="295" height="250" rx="8" fill="#ffffff" stroke="#e5e7eb"/>
  
  <!-- 모바일 차트 -->
  <text x="50" y="245" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#111827">월별 매출 추이</text>
  
  <!-- 간단한 차트 -->
  <line x1="60" y1="260" x2="60" y2="450" stroke="#d1d5db" stroke-width="2"/>
  <line x1="60" y1="450" x2="315" y2="450" stroke="#d1d5db" stroke-width="2"/>
  
  <!-- 데이터 포인트 -->
  <circle cx="120" cy="400" r="3" fill="#2563eb"/>
  <circle cx="187" cy="360" r="3" fill="#2563eb"/>
  <circle cx="254" cy="320" r="3" fill="#2563eb"/>
  
  <polyline points="120,400 187,360 254,320" fill="none" stroke="#2563eb" stroke-width="2"/>
  
  <!-- 레이블 -->
  <text x="120" y="415" font-family="Arial, sans-serif" font-size="8" fill="#111827" text-anchor="middle">11월</text>
  <text x="187" y="415" font-family="Arial, sans-serif" font-size="8" fill="#111827" text-anchor="middle">12월</text>
  <text x="254" y="415" font-family="Arial, sans-serif" font-size="8" fill="#111827" text-anchor="middle">1월</text>
  
  <text x="120" y="395" font-family="Arial, sans-serif" font-size="8" fill="#111827" text-anchor="middle">125K</text>
  <text x="187" y="355" font-family="Arial, sans-serif" font-size="8" fill="#111827" text-anchor="middle">142K</text>
  <text x="254" y="315" font-family="Arial, sans-serif" font-size="8" fill="#111827" text-anchor="middle">159K</text>
  
  <!-- 모바일 액션 버튼들 -->
  <rect x="40" y="490" width="295" height="40" rx="8" fill="#f9fafb"/>
  
  <rect x="60" y="500" width="60" height="20" rx="10" fill="#2563eb"/>
  <text x="90" y="512" font-family="Arial, sans-serif" font-size="8" fill="#ffffff" text-anchor="middle">📥 내보내기</text>
  
  <rect x="130" y="500" width="60" height="20" rx="10" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="160" y="512" font-family="Arial, sans-serif" font-size="8" fill="#374151" text-anchor="middle">🔗 공유</text>
  
  <rect x="200" y="500" width="60" height="20" rx="10" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="230" y="512" font-family="Arial, sans-serif" font-size="8" fill="#374151" text-anchor="middle">📊 상세보기</text>
  
  <!-- 추가 분석 제안 -->
  <rect x="40" y="550" width="295" height="80" rx="8" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="50" y="570" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#374151">🔍 추가 분석 제안</text>
  
  <rect x="50" y="580" width="275" height="20" rx="4" fill="#ffffff" stroke="#d1d5db"/>
  <text x="55" y="592" font-family="Arial, sans-serif" font-size="9" fill="#6b7280">"제품별 매출 분석을 해보시는 것은 어떨까요?"</text>
  
  <rect x="50" y="605" width="275" height="20" rx="4" fill="#ffffff" stroke="#d1d5db"/>
  <text x="55" y="617" font-family="Arial, sans-serif" font-size="9" fill="#6b7280">"고객 세그먼트별 매출 비교 분석"</text>
</svg>

## 🔄 로딩 상태 화면

<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <!-- 배경 -->
  <rect width="400" height="300" fill="#f9fafb" rx="12"/>
  
  <!-- 로딩 스피너 -->
  <circle cx="200" cy="120" r="20" fill="none" stroke="#e5e7eb" stroke-width="4"/>
  <circle cx="200" cy="120" r="20" fill="none" stroke="#2563eb" stroke-width="4" stroke-linecap="round" stroke-dasharray="31.416" stroke-dashoffset="7.854">
    <animateTransform attributeName="transform" type="rotate" values="0 200 120;360 200 120" dur="1s" repeatCount="indefinite"/>
  </circle>
  
  <!-- 로딩 텍스트 -->
  <text x="200" y="170" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#111827" text-anchor="middle">분석 중입니다...</text>
  <text x="200" y="190" font-family="Arial, sans-serif" font-size="12" fill="#6b7280" text-anchor="middle">질문을 분석하고 있습니다</text>
  
  <!-- 프로그레스 바 -->
  <rect x="120" y="210" width="160" height="8" rx="4" fill="#e5e7eb"/>
  <rect x="120" y="210" width="80" height="8" rx="4" fill="#2563eb">
    <animate attributeName="width" values="0;160;0" dur="3s" repeatCount="indefinite"/>
  </rect>
  
  <!-- 단계 표시 -->
  <text x="200" y="240" font-family="Arial, sans-serif" font-size="10" fill="#9ca3af" text-anchor="middle">1/4 단계: 자연어 분석</text>
</svg>

## ❌ 오류 상태 화면

<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <!-- 배경 -->
  <rect width="400" height="300" fill="#ffffff" rx="12" stroke="#ef4444" stroke-width="1"/>
  
  <!-- 오류 아이콘 -->
  <circle cx="200" cy="80" r="25" fill="#fef2f2"/>
  <text x="200" y="90" font-family="Arial, sans-serif" font-size="30" fill="#ef4444" text-anchor="middle">⚠️</text>
  
  <!-- 오류 메시지 -->
  <text x="200" y="130" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#ef4444" text-anchor="middle">분석 중 오류가 발생했습니다</text>
  
  <!-- 오류 상세 -->
  <rect x="50" y="145" width="300" height="40" rx="6" fill="#f9fafb"/>
  <text x="60" y="160" font-family="Arial, sans-serif" font-size="10" fill="#6b7280">오류 코드: DB_CONNECTION_FAILED</text>
  <text x="60" y="175" font-family="Arial, sans-serif" font-size="10" fill="#6b7280">데이터베이스 연결에 실패했습니다. 잠시 후 다시 시도해주세요.</text>
  
  <!-- 액션 버튼들 -->
  <rect x="120" y="210" width="70" height="30" rx="15" fill="#2563eb"/>
  <text x="155" y="228" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">다시 시도</text>
  
  <rect x="210" y="210" width="70" height="30" rx="15" fill="#f3f4f6" stroke="#d1d5db"/>
  <text x="245" y="228" font-family="Arial, sans-serif" font-size="12" fill="#374151" text-anchor="middle">도움말</text>
</svg>

## 📝 사이드바 (모바일 오픈 상태)

<svg width="375" height="667" viewBox="0 0 375 667" xmlns="http://www.w3.org/2000/svg">
  <!-- 오버레이 -->
  <rect width="375" height="667" fill="rgba(0,0,0,0.5)"/>
  
  <!-- 사이드바 -->
  <rect x="0" y="0" width="280" height="667" fill="#f9fafb"/>
  
  <!-- 사이드바 헤더 -->
  <rect x="0" y="0" width="280" height="60" fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>
  <text x="20" y="35" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#2563eb">🧞‍♂️ DataGenie</text>
  <text x="240" y="35" font-family="Arial, sans-serif" font-size="18" fill="#6b7280">×</text>
  
  <!-- 사이드바 컨텐츠 -->
  <text x="20" y="90" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#374151">📜 최근 질문</text>
  
  <!-- 질문 이력 -->
  <rect x="20" y="100" width="240" height="35" rx="6" fill="#ffffff" stroke="#e5e7eb"/>
  <text x="30" y="115" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#111827">지난 3개월 매출 현황</text>
  <text x="30" y="127" font-family="Arial, sans-serif" font-size="8" fill="#6b7280">2024-01-15 • 성공</text>
  
  <rect x="20" y="140" width="240" height="35" rx="6" fill="#ffffff" stroke="#e5e7eb"/>
  <text x="30" y="155" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#111827">월별 고객 증가율</text>
  <text x="30" y="167" font-family="Arial, sans-serif" font-size="8" fill="#6b7280">2024-01-14 • 성공</text>
  
  <!-- 즐겨찾기 섹션 -->
  <line x1="20" y1="190" x2="260" y2="190" stroke="#e5e7eb"/>
  <text x="20" y="215" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#374151">⭐ 즐겨찾기</text>
  
  <rect x="20" y="225" width="240" height="30" rx="6" fill="#ffffff" stroke="#e5e7eb"/>
  <text x="30" y="243" font-family="Arial, sans-serif" font-size="10" font-weight="500" fill="#111827">월별 매출 대시보드</text>
  
  <!-- 설정 섹션 -->
  <line x1="20" y1="270" x2="260" y2="270" stroke="#e5e7eb"/>
  <text x="20" y="295" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#374151">⚙️ 빠른 설정</text>
  
  <rect x="20" y="305" width="12" height="12" rx="2" fill="#2563eb"/>
  <text x="40" y="315" font-family="Arial, sans-serif" font-size="11" fill="#374151">자동 시각화</text>
  
  <rect x="20" y="325" width="240" height="20" rx="4" fill="#ffffff" stroke="#d1d5db"/>
  <text x="25" y="337" font-family="Arial, sans-serif" font-size="9" fill="#6b7280">기본 차트: 자동 선택</text>
</svg>

---

## 📱 터치 인터랙션 가이드

<svg width="200" height="100" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
  <!-- 터치 영역 예시 -->
  <rect x="50" y="25" width="100" height="50" rx="8" fill="#2563eb" opacity="0.1" stroke="#2563eb" stroke-dasharray="2,2"/>
  <rect x="60" y="35" width="80" height="30" rx="4" fill="#2563eb"/>
  <text x="100" y="52" font-family="Arial, sans-serif" font-size="12" fill="#ffffff" text-anchor="middle">버튼</text>
  
  <!-- 최소 터치 영역 표시 -->
  <text x="100" y="15" font-family="Arial, sans-serif" font-size="8" fill="#6b7280" text-anchor="middle">최소 44px × 44px 터치 영역</text>
  <text x="100" y="85" font-family="Arial, sans-serif" font-size="8" fill="#6b7280" text-anchor="middle">터치 친화적 디자인</text>
</svg>

## ♿ 접근성 가이드

<svg width="300" height="150" viewBox="0 0 300 150" xmlns="http://www.w3.org/2000/svg">
  <!-- 포커스 표시 예시 -->
  <rect x="50" y="30" width="80" height="30" rx="4" fill="#2563eb"/>
  <rect x="47" y="27" width="86" height="36" rx="6" fill="none" stroke="#2563eb" stroke-width="2" stroke-dasharray="3,3"/>
  <text x="90" y="47" font-family="Arial, sans-serif" font-size="10" fill="#ffffff" text-anchor="middle">포커스 버튼</text>
  
  <!-- 색상 대비 예시 -->
  <rect x="170" y="30" width="80" height="30" rx="4" fill="#0000ee"/>
  <text x="210" y="47" font-family="Arial, sans-serif" font-size="10" fill="#ffffff" text-anchor="middle">고대비 버튼</text>
  
  <!-- 설명 텍스트 -->
  <text x="20" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#374151">접근성 표시</text>
  <text x="50" y="80" font-family="Arial, sans-serif" font-size="9" fill="#6b7280">키보드 포커스</text>
  <text x="170" y="80" font-family="Arial, sans-serif" font-size="9" fill="#6b7280">고대비 모드</text>
  
  <!-- 스크린 리더 안내 -->
  <rect x="50" y="100" width="200" height="30" rx="4" fill="#f9fafb" stroke="#e5e7eb"/>
  <text x="60" y="115" font-family="Arial, sans-serif" font-size="9" fill="#374151">🔊 스크린 리더 텍스트: "분석 시작 버튼"</text>
</svg>

## 📊 반응형 그리드 시스템

<svg width="600" height="200" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
  <!-- 데스크톱 레이아웃 -->
  <text x="10" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#374151">데스크톱 (1200px+)</text>
  <rect x="10" y="30" width="60" height="80" fill="#e5e7eb" stroke="#d1d5db"/>
  <text x="40" y="75" font-family="Arial, sans-serif" font-size="8" fill="#6b7280" text-anchor="middle">사이드바</text>
  <rect x="80" y="30" width="120" height="80" fill="#2563eb" opacity="0.1" stroke="#2563eb"/>
  <text x="140" y="75" font-family="Arial, sans-serif" font-size="8" fill="#374151" text-anchor="middle">메인 컨텐츠</text>
  
  <!-- 태블릿 레이아웃 -->
  <text x="220" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#374151">태블릿 (768px-1199px)</text>
  <rect x="220" y="30" width="50" height="80" fill="#e5e7eb" stroke="#d1d5db"/>
  <rect x="280" y="30" width="100" height="80" fill="#2563eb" opacity="0.1" stroke="#2563eb"/>
  
  <!-- 모바일 레이아웃 -->
  <text x="400" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#374151">모바일 (767px 이하)</text>
  <rect x="400" y="30" width="150" height="80" fill="#2563eb" opacity="0.1" stroke="#2563eb"/>
  <text x="475" y="75" font-family="Arial, sans-serif" font-size="8" fill="#374151" text-anchor="middle">전체 화면</text>
  
  <!-- 사이드바 오버레이 표시 -->
  <rect x="560" y="30" width="30" height="80" fill="#374151" opacity="0.8"/>
  <text x="575" y="75" font-family="Arial, sans-serif" font-size="6" fill="#ffffff" text-anchor="middle">사이드바<br/>(오버레이)</text>
  
  <!-- 브레이크포인트 표시 -->
  <line x1="10" y1="140" x2="590" y2="140" stroke="#d1d5db"/>
  <text x="40" y="155" font-family="Arial, sans-serif" font-size="8" fill="#6b7280" text-anchor="middle">1200px</text>
  <text x="300" y="155" font-family="Arial, sans-serif" font-size="8" fill="#6b7280" text-anchor="middle">768px</text>
  <text x="475" y="155" font-family="Arial, sans-serif" font-size="8" fill="#6b7280" text-anchor="middle">480px</text>
</svg>

