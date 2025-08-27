"""
DataGenie Frontend Launcher

Gradio 웹 인터페이스를 실행하는 런처입니다.
"""

import os
import sys
import asyncio
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.frontend.gradio_app import create_app
from app.frontend.services import DataGenieAPIService


async def check_backend_status():
    """백엔드 서버 상태 확인"""
    api_service = DataGenieAPIService()
    try:
        status = await api_service.health_check()
        await api_service.close_session()
        return status
    except Exception as e:
        print(f"백엔드 연결 확인 중 오류: {e}")
        return False


def main():
    """메인 실행 함수"""
    print("🧞‍♂️ DataGenie 웹 인터페이스를 시작합니다...")
    
    # 백엔드 상태 확인
    print("📡 백엔드 서버 연결 확인 중...")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    backend_available = loop.run_until_complete(check_backend_status())
    
    if backend_available:
        print("✅ 백엔드 서버 연결 성공!")
        print("🔗 API 연동 모드로 실행됩니다.")
    else:
        print("⚠️  백엔드 서버에 연결할 수 없습니다.")
        print("🎭 데모 모드로 실행됩니다.")
    
    # Gradio 앱 생성 및 실행
    print("🚀 웹 인터페이스를 시작합니다...")
    
    app = create_app()
    
    # 환경 변수에서 설정 읽기
    host = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    share = os.getenv("GRADIO_SHARE", "false").lower() == "true"
    
    print(f"🌐 서버 주소: http://{host}:{port}")
    print(f"🔗 로컬 접속: http://localhost:{port}")
    
    if share:
        print("🌍 공유 링크가 생성됩니다...")
    
    try:
        app.launch(
            server_name=host,
            server_port=port,
            share=share,
            debug=False,
            show_error=True,
            quiet=False
        )
    except KeyboardInterrupt:
        print("\n👋 DataGenie 웹 인터페이스를 종료합니다.")
    except Exception as e:
        print(f"❌ 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
