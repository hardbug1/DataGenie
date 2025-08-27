"""
DataGenie Gradio Web Interface

사용자 친화적인 웹 인터페이스를 제공하는 Gradio 애플리케이션입니다.
Clean Architecture: Interface Layer
"""

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, Tuple, Dict, Any, List
import requests
import json
import os
from datetime import datetime

from .services import DataGenieAPIService, DemoDataService, HistoryService

# 백엔드 API 설정
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class DataGenieUI:
    """DataGenie Gradio 웹 인터페이스"""
    
    def __init__(self):
        """UI 초기화"""
        self.api_service = DataGenieAPIService(API_BASE_URL)
        self.demo_service = DemoDataService()
        self.history_service = HistoryService()
        self.use_demo_mode = True  # 백엔드 연결 실패시 데모 모드 사용
        
    def setup_interface(self) -> gr.Blocks:
        """Gradio 인터페이스 설정"""
        
        # 🚀 2024 최신 디자인 트렌드 - Ultra Modern UI
        custom_css = """
        /* === 2024 최신 디자인 시스템 === */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        :root {
            /* 2024 최신 컬러 팔레트 */
            --primary: #6366f1;
            --primary-light: #8b5cf6;
            --primary-dark: #4f46e5;
            --secondary: #f59e0b;
            --accent: #06b6d4;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            
            /* 뉴모피즘 컬러 */
            --glass-white: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --glass-shadow: rgba(0, 0, 0, 0.1);
            
            /* 최신 타이포그래피 */
            --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
            
            /* 현대적 간격 시스템 */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            --space-3xl: 4rem;
        }
        
        /* === 글로벌 리셋 및 기본 스타일 === */
        * {
            font-family: var(--font-primary) !important;
            box-sizing: border-box !important;
            margin: 0;
            padding: 0;
        }
        
        html, body {
            scroll-behavior: smooth;
            font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
        }
        
        /* === 메인 컨테이너 - 2024 트렌드 배경 === */
        .gradio-container {
            max-width: 1800px !important;
            margin: 0 auto !important;
            background: 
                /* 메인 그라데이션 */
                linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%),
                /* 오버레이 패턴 */
                radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(255,255,255,0.05) 0%, transparent 50%) !important;
            background-size: 400% 400%, 100% 100%, 100% 100% !important;
            background-attachment: fixed !important;
            animation: gradient-shift 15s ease infinite !important;
            min-height: 100vh !important;
            padding: var(--space-xl) !important;
            position: relative !important;
            overflow-x: hidden !important;
        }
        
        /* 배경 애니메이션 */
        @keyframes gradient-shift {
            0%, 100% { background-position: 0% 50%, 0% 0%, 0% 0%; }
            50% { background-position: 100% 50%, 100% 100%, 100% 100%; }
        }
        
        /* === 플로팅 장식 요소 === */
        .gradio-container::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.3) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.2) 0%, transparent 40%),
                radial-gradient(circle at 60% 40%, rgba(14, 165, 233, 0.15) 0%, transparent 30%);
            pointer-events: none;
            z-index: 0;
            animation: float-shapes 20s ease-in-out infinite;
        }
        
        @keyframes float-shapes {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
            50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
        }
        
        /* === 메인 콘텐츠 컨테이너 === */
        .gradio-container > * {
            position: relative;
            z-index: 1;
        }
        
        /* === 🎨 2024 Ultra Modern 헤더 === */
        .main-header {
            background: 
                /* 그라디언트 글래스 효과 */
                linear-gradient(135deg, 
                    rgba(255, 255, 255, 0.25) 0%, 
                    rgba(255, 255, 255, 0.1) 50%, 
                    rgba(255, 255, 255, 0.05) 100%),
                /* 노이즈 텍스처 */
                url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
            backdrop-filter: blur(40px) saturate(200%) contrast(120%);
            -webkit-backdrop-filter: blur(40px) saturate(200%) contrast(120%);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: var(--space-3xl) var(--space-2xl);
            border-radius: 32px;
            margin-bottom: var(--space-3xl);
            box-shadow: 
                /* 메인 그림자 */
                0 32px 64px rgba(0, 0, 0, 0.25),
                /* 테두리 하이라이트 */
                inset 0 1px 0 rgba(255, 255, 255, 0.4),
                /* 상단 그로우 */
                0 0 0 1px rgba(255, 255, 255, 0.1),
                /* 내부 발광 */
                inset 0 0 32px rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
            transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
            transform-origin: center;
        }
        
        .main-header:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                /* 메인 호버 그림자 */
                0 48px 100px rgba(0, 0, 0, 0.3),
                /* 글로우 효과 */
                0 0 60px rgba(99, 102, 241, 0.4),
                /* 테두리 강화 */
                inset 0 1px 0 rgba(255, 255, 255, 0.6),
                /* 외부 링 */
                0 0 0 1px rgba(255, 255, 255, 0.2);
        }
        
        /* 동적 배경 애니메이션 */
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: 
                conic-gradient(from 0deg at 50% 50%, 
                    transparent 0deg, 
                    rgba(255, 255, 255, 0.1) 60deg, 
                    transparent 120deg, 
                    rgba(255, 255, 255, 0.05) 180deg, 
                    transparent 240deg, 
                    rgba(255, 255, 255, 0.1) 300deg, 
                    transparent 360deg);
            animation: rotate-conic 20s linear infinite;
            pointer-events: none;
            opacity: 0.7;
        }
        
        /* 반짝이는 하이라이트 */
        .main-header::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                110deg, 
                transparent 0%, 
                rgba(255, 255, 255, 0.4) 45%, 
                rgba(255, 255, 255, 0.6) 50%, 
                rgba(255, 255, 255, 0.4) 55%, 
                transparent 100%
            );
            animation: luxury-shine 4s ease-in-out infinite;
            pointer-events: none;
        }
        
        @keyframes rotate-conic {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes luxury-shine {
            0%, 100% { left: -100%; opacity: 0; }
            50% { left: 100%; opacity: 1; }
        }
        
        /* === 🎨 Ultra Modern 헤더 텍스트 === */
        .main-header h1 {
            font-size: 4rem !important;
            font-weight: 900 !important;
            margin: 0 !important;
            background: 
                linear-gradient(135deg, 
                    #ffffff 0%, 
                    #f8fafc 25%, 
                    #e2e8f0 50%, 
                    #ffffff 75%, 
                    #f1f5f9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            background-size: 200% 200%;
            animation: text-shimmer 3s ease-in-out infinite;
            letter-spacing: -0.04em;
            line-height: 1.1;
            position: relative;
            z-index: 2;
            text-shadow: 
                0 1px 3px rgba(0, 0, 0, 0.3),
                0 4px 8px rgba(0, 0, 0, 0.2);
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.5));
        }
        
        /* 텍스트 애니메이션 */
        @keyframes text-shimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        /* 라이브 상태 인디케이터 */
        .main-header h1::after {
            content: '';
            position: absolute;
            top: 15%;
            right: -2rem;
            width: 12px;
            height: 12px;
            background: 
                radial-gradient(circle, 
                    #10b981 0%, 
                    #34d399 50%, 
                    transparent 70%);
            border-radius: 50%;
            box-shadow: 
                0 0 20px #10b981,
                0 0 40px #10b981,
                inset 0 0 10px rgba(255, 255, 255, 0.5);
            animation: live-pulse 2s ease-in-out infinite;
        }
        
        @keyframes live-pulse {
            0%, 100% { 
                opacity: 0.8; 
                transform: translateY(-50%) scale(1);
                box-shadow: 
                    0 0 20px #10b981,
                    0 0 40px #10b981;
            }
            50% { 
                opacity: 1; 
                transform: translateY(-50%) scale(1.3);
                box-shadow: 
                    0 0 30px #10b981,
                    0 0 60px #10b981,
                    0 0 80px rgba(16, 185, 129, 0.5);
            }
        }
        
        .main-header p {
            font-size: 1.5rem !important;
            margin: 1.5rem 0 0 0 !important;
            opacity: 0.95;
            font-weight: 500;
            letter-spacing: 0.02em;
            line-height: 1.5;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            animation: fade-in-up 1s ease-out 0.5s both;
        }
        
        @keyframes fade-in-up {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 0.95;
                transform: translateY(0);
            }
        }
        
        /* === 🚀 2024 Ultra Modern 카드 시스템 === */
        .gr-box, .gr-form, .gr-panel {
            background: 
                /* 메인 글래스 그라디언트 */
                linear-gradient(145deg, 
                    rgba(255, 255, 255, 0.95) 0%, 
                    rgba(255, 255, 255, 0.8) 50%,
                    rgba(255, 255, 255, 0.9) 100%),
                /* 노이즈 오버레이 */
                url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E") !important;
            
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 24px !important;
            
            box-shadow: 
                /* 메인 드롭 섀도우 */
                0 20px 50px rgba(0, 0, 0, 0.1),
                /* 서브틀 내부 섀도우 */
                inset 0 1px 0 rgba(255, 255, 255, 0.8),
                /* 외부 하이라이트 */
                0 0 0 1px rgba(255, 255, 255, 0.1),
                /* 글로우 효과 */
                0 0 30px rgba(99, 102, 241, 0.05) !important;
                
            backdrop-filter: blur(25px) saturate(180%) contrast(110%) !important;
            -webkit-backdrop-filter: blur(25px) saturate(180%) contrast(110%) !important;
            
            margin: var(--space-xl) 0 !important;
            padding: var(--space-2xl) !important;
            
            transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1) !important;
            position: relative !important;
            overflow: hidden !important;
            
            /* 3D 변형 준비 */
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        /* 동적 테두리 애니메이션 */
        .gr-box::before, .gr-form::before, .gr-panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: 
                linear-gradient(90deg, 
                    transparent 0%, 
                    rgba(99, 102, 241, 0.6) 25%,
                    rgba(168, 85, 247, 0.6) 50%,
                    rgba(236, 72, 153, 0.6) 75%,
                    transparent 100%);
            border-radius: 24px 24px 0 0;
            animation: border-flow 3s ease-in-out infinite;
        }
        
        @keyframes border-flow {
            0%, 100% { opacity: 0.3; transform: scaleX(0.8); }
            50% { opacity: 1; transform: scaleX(1.1); }
        }
        
        /* 마이크로 인터랙션 호버 효과 */
        .gr-box:hover, .gr-form:hover, .gr-panel:hover {
            transform: translateY(-8px) rotateX(2deg) scale(1.02);
            
            box-shadow: 
                /* 강화된 드롭 섀도우 */
                0 40px 80px rgba(0, 0, 0, 0.15),
                /* 글로우 증강 */
                0 0 60px rgba(99, 102, 241, 0.2),
                /* 내부 하이라이트 강화 */
                inset 0 1px 0 rgba(255, 255, 255, 1),
                /* 외부 링 강화 */
                0 0 0 1px rgba(99, 102, 241, 0.3) !important;
                
            border-color: rgba(99, 102, 241, 0.5) !important;
            
            /* 호버시 배경 변화 */
            background: 
                linear-gradient(145deg, 
                    rgba(255, 255, 255, 0.98) 0%, 
                    rgba(248, 250, 252, 0.95) 50%,
                    rgba(255, 255, 255, 0.98) 100%) !important;
        }
        
        /* 포커스 상태 */
        .gr-box:focus-within, .gr-form:focus-within, .gr-panel:focus-within {
            border-color: rgba(99, 102, 241, 0.6) !important;
            box-shadow: 
                0 0 0 4px rgba(99, 102, 241, 0.1),
                0 20px 50px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        }
        
        /* 프리미엄 입력 필드 */
        .gr-textbox, .gr-textarea {
            border: 1px solid rgba(148, 163, 184, 0.3) !important;
            border-radius: 16px !important;
            font-size: 16px !important;
            padding: 1.25rem 1.5rem !important;
            background: linear-gradient(145deg, 
                rgba(255, 255, 255, 0.95) 0%, 
                rgba(248, 250, 252, 0.9) 100%) !important;
            color: #1e293b !important;
            font-weight: 500 !important;
            line-height: 1.6 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 1px 3px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .gr-textbox:focus, .gr-textarea:focus {
            border-color: rgba(99, 102, 241, 0.6) !important;
            background: rgba(255, 255, 255, 0.98) !important;
            box-shadow: 
                0 0 0 4px rgba(99, 102, 241, 0.1),
                0 4px 20px rgba(99, 102, 241, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 1) !important;
            outline: none !important;
            transform: translateY(-1px) !important;
        }
        
        .gr-textbox::placeholder, .gr-textarea::placeholder {
            color: #94a3b8 !important;
            font-weight: 400 !important;
        }
        
        /* === 🎨 2024 Luxury 버튼 시스템 === */
        .gr-button {
            background: 
                linear-gradient(135deg, 
                    #6366f1 0%, 
                    #8b5cf6 30%,
                    #a855f7 60%, 
                    #d946ef 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 16px !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 0.875rem 1.75rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 4px 15px rgba(99, 102, 241, 0.4),
                0 2px 4px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            text-transform: none !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .gr-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(255, 255, 255, 0.2) 50%, 
                transparent 100%);
            transition: left 0.5s;
        }
        
        .gr-button:hover {
            background: linear-gradient(135deg, 
                #4f46e5 0%, 
                #7c3aed 50%, 
                #c026d3 100%) !important;
            transform: translateY(-2px) scale(1.05) !important;
            box-shadow: 
                0 8px 25px rgba(99, 102, 241, 0.5),
                0 4px 8px rgba(0, 0, 0, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        }
        
        .gr-button:hover::before {
            left: 100%;
        }
        
        .gr-button:active {
            transform: translateY(0) scale(1.02) !important;
        }
        
        .gr-button.gr-button-lg {
            font-size: 18px !important;
            padding: 1.25rem 2.5rem !important;
            font-weight: 700 !important;
            border-radius: 20px !important;
            background: linear-gradient(135deg, 
                #059669 0%, 
                #10b981 50%, 
                #34d399 100%) !important;
            box-shadow: 
                0 6px 20px rgba(16, 185, 129, 0.4),
                0 3px 6px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        }
        
        .gr-button.gr-button-lg:hover {
            background: linear-gradient(135deg, 
                #047857 0%, 
                #059669 50%, 
                #10b981 100%) !important;
            box-shadow: 
                0 10px 30px rgba(16, 185, 129, 0.5),
                0 5px 10px rgba(0, 0, 0, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        }
        
        .gr-button.gr-button-sm {
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.9) 0%, 
                rgba(248, 250, 252, 0.8) 100%) !important;
            color: #475569 !important;
            font-size: 13px !important;
            padding: 0.625rem 1.25rem !important;
            box-shadow: 
                0 2px 8px rgba(0, 0, 0, 0.08),
                0 1px 2px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
        }
        
        .gr-button.gr-button-sm:hover {
            background: linear-gradient(135deg, 
                #6366f1 0%, 
                #8b5cf6 100%) !important;
            color: white !important;
            box-shadow: 
                0 4px 15px rgba(99, 102, 241, 0.3),
                0 2px 4px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            border-color: rgba(99, 102, 241, 0.3) !important;
        }
        
        /* 프리미엄 탭 스타일 */
        .gr-tabs {
            background: transparent !important;
            margin: 2rem 0 !important;
        }
        
        .gr-tab-nav {
            background: linear-gradient(145deg, 
                rgba(255, 255, 255, 0.95) 0%, 
                rgba(248, 250, 252, 0.9) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 18px !important;
            padding: 0.75rem !important;
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.1),
                0 3px 6px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(20px) !important;
        }
        
        .gr-tab-nav button {
            background: transparent !important;
            border: none !important;
            border-radius: 12px !important;
            color: #64748b !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 1rem 1.75rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .gr-tab-nav button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(99, 102, 241, 0.1) 50%, 
                transparent 100%);
            transition: left 0.5s;
        }
        
        .gr-tab-nav button:hover {
            background: rgba(99, 102, 241, 0.05) !important;
            color: #4f46e5 !important;
            transform: translateY(-1px) !important;
        }
        
        .gr-tab-nav button:hover::before {
            left: 100%;
        }
        
        .gr-tab-nav button.selected {
            background: linear-gradient(135deg, 
                #6366f1 0%, 
                #8b5cf6 50%, 
                #d946ef 100%) !important;
            color: white !important;
            box-shadow: 
                0 4px 15px rgba(99, 102, 241, 0.4),
                0 2px 4px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            transform: translateY(-2px) !important;
        }
        
        .gr-tab-nav button.selected::before {
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(255, 255, 255, 0.2) 50%, 
                transparent 100%);
        }
        
        /* 라벨 및 텍스트 */
        .gr-form label, .gr-box label {
            color: #1f2937 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* 프리미엄 섹션 헤더 스타일 */
        .section-header {
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.8) 0%, 
                rgba(248, 250, 252, 0.6) 100%) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(99, 102, 241, 0.2) !important;
            padding: 1.5rem 2rem !important;
            border-radius: 16px !important;
            margin: 1.5rem 0 1rem 0 !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .section-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(135deg, 
                #6366f1 0%, 
                #8b5cf6 50%, 
                #d946ef 100%);
            border-radius: 0 4px 4px 0;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(99, 102, 241, 0.1) 100%);
            pointer-events: none;
        }
        
        .section-header h3 {
            color: #1e293b !important;
            font-weight: 700 !important;
            font-size: 1.2rem !important;
            margin: 0 !important;
            position: relative !important;
            z-index: 1 !important;
            background: linear-gradient(135deg, 
                #1e293b 0%, 
                #4f46e5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .gr-markdown {
            color: #1f2937 !important;
            line-height: 1.7 !important;
        }
        
        .gr-markdown h1, .gr-markdown h2, .gr-markdown h3 {
            color: #111827 !important;
            font-weight: 700 !important;
            margin: 1.5rem 0 1rem 0 !important;
        }
        
        .gr-markdown h1 { font-size: 1.8rem !important; }
        .gr-markdown h2 { font-size: 1.5rem !important; }
        .gr-markdown h3 { font-size: 1.3rem !important; }
        
        /* 프리미엄 상태 표시 */
        .status-success {
            background: linear-gradient(135deg, 
                #10b981 0%, 
                #059669 50%, 
                #34d399 100%);
            color: white !important;
            padding: 1.25rem 2rem;
            border-radius: 16px;
            font-weight: 600 !important;
            font-size: 15px !important;
            box-shadow: 
                0 8px 25px rgba(16, 185, 129, 0.4),
                0 3px 6px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .status-success::before {
            content: '✨';
            position: absolute;
            right: 1rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2rem;
            animation: sparkle 2s infinite;
        }
        
        .status-error {
            background: linear-gradient(135deg, 
                #ef4444 0%, 
                #dc2626 50%, 
                #f87171 100%);
            color: white !important;
            padding: 1.25rem 2rem;
            border-radius: 16px;
            font-weight: 600 !important;
            font-size: 15px !important;
            box-shadow: 
                0 8px 25px rgba(239, 68, 68, 0.4),
                0 3px 6px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        }
        
        .status-processing {
            background: linear-gradient(135deg, 
                #f59e0b 0%, 
                #d97706 50%, 
                #fbbf24 100%);
            color: white !important;
            padding: 1.25rem 2rem;
            border-radius: 16px;
            font-weight: 600 !important;
            font-size: 15px !important;
            box-shadow: 
                0 8px 25px rgba(245, 158, 11, 0.4),
                0 3px 6px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            animation: pulse-glow 2s infinite;
            position: relative;
            overflow: hidden;
        }
        
        .status-processing::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(255, 255, 255, 0.3) 50%, 
                transparent 100%);
            animation: loading-shine 1.5s infinite;
        }
        
        @keyframes pulse-glow {
            0%, 100% { 
                opacity: 1; 
                box-shadow: 
                    0 8px 25px rgba(245, 158, 11, 0.4),
                    0 3px 6px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }
            50% { 
                opacity: 0.9; 
                box-shadow: 
                    0 12px 35px rgba(245, 158, 11, 0.6),
                    0 5px 10px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
            }
        }
        
        @keyframes loading-shine {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        @keyframes sparkle {
            0%, 100% { transform: translateY(-50%) scale(1) rotate(0deg); }
            50% { transform: translateY(-50%) scale(1.2) rotate(180deg); }
        }
        
        /* 프리미엄 이력 카드 */
        .history-item {
            background: linear-gradient(145deg, 
                rgba(255, 255, 255, 0.95) 0%, 
                rgba(248, 250, 252, 0.9) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 
                0 6px 20px rgba(0, 0, 0, 0.08),
                0 2px 4px rgba(0, 0, 0, 0.03),
                inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .history-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
            background: linear-gradient(135deg, 
                #6366f1 0%, 
                #8b5cf6 50%, 
                #d946ef 100%);
            border-radius: 0 3px 3px 0;
        }
        
        .history-item:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 
                0 12px 30px rgba(0, 0, 0, 0.15),
                0 4px 8px rgba(0, 0, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 1) !important;
            border-color: rgba(99, 102, 241, 0.3) !important;
        }
        
        .history-item strong {
            color: #1e293b !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
            display: block !important;
            margin-bottom: 0.5rem !important;
        }
        
        .history-item small {
            color: #64748b !important;
            font-size: 12px !important;
            font-weight: 500 !important;
        }
        
        /* 데이터 테이블 */
        .gr-dataframe {
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }
        
        .gr-dataframe table {
            font-size: 14px !important;
            color: #374151 !important;
        }
        
        .gr-dataframe th {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
            color: #1f2937 !important;
            font-weight: 600 !important;
            padding: 1rem !important;
        }
        
        .gr-dataframe td {
            padding: 0.75rem 1rem !important;
            border-bottom: 1px solid #f1f5f9 !important;
        }
        
        /* 플롯 영역 */
        .gr-plot {
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* 코드 블록 */
        .gr-code {
            border-radius: 12px !important;
            background: #1f2937 !important;
            color: #f9fafb !important;
            font-family: 'Fira Code', 'Monaco', 'Consolas', monospace !important;
            font-size: 13px !important;
            line-height: 1.6 !important;
        }
        
        /* 스크롤바 */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
        }
        
        /* 반응형 디자인 */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem !important;
            }
            
            .main-header p {
                font-size: 1rem !important;
            }
            
            .gr-box, .gr-form, .gr-panel {
                margin: 0.5rem 0 !important;
            }
        }
        """
        
        # 2024 최신 트렌드 테마 생성 - 호환성 개선
        modern_theme = gr.themes.Base(
            primary_hue=gr.themes.colors.violet,
            secondary_hue=gr.themes.colors.pink,
            neutral_hue=gr.themes.colors.slate,
            font=[
                gr.themes.GoogleFont("Inter"),
                "ui-sans-serif",
                "system-ui",
                "sans-serif"
            ]
        )

        with gr.Blocks(
            title="🧞‍♂️ DataGenie - AI 데이터 분석 비서",
            theme=modern_theme,
            css=custom_css,
            head="""
            <style>
                /* CSS 우선순위를 높이기 위한 추가 스타일 */
                .gradio-container { 
                    font-family: 'Inter', sans-serif !important;
                }
            </style>
            """
        ) as app:
            
            # 상태 변수들
            session_state = gr.State({})
            
            # 메인 헤더 - 개선된 디자인
            with gr.Row():
                gr.HTML("""
                <div class="main-header">
                    <h1>🧞‍♂️ DataGenie</h1>
                    <p>AI 데이터 분석 비서 - 자연어로 질문하고 인사이트를 얻으세요</p>
                </div>
                """)
            
            with gr.Row():
                # 왼쪽 컬럼 - 질문 입력 및 설정
                with gr.Column(scale=2):
                    
                    # 질문 입력 영역
                    with gr.Group():
                        gr.Markdown("### 💬 무엇을 알고 싶으신가요?", elem_classes=["section-header"])
                        
                        question_input = gr.Textbox(
                            label="질문을 입력하세요",
                            placeholder="예: 지난 3개월 매출 현황을 차트로 보여주세요",
                            lines=3,
                            elem_classes=["question-input"]
                        )
                        
                        # 예시 질문 버튼들
                        with gr.Row():
                            example_btn1 = gr.Button("📊 월별 매출 현황", size="sm")
                            example_btn2 = gr.Button("📈 성장률 분석", size="sm")
                            example_btn3 = gr.Button("🎯 고객 세분화", size="sm")
                    
                    # 데이터 소스 선택
                    with gr.Group():
                        gr.Markdown("### 🗄️ 데이터 소스 선택", elem_classes=["section-header"])
                        
                        data_source_type = gr.Radio(
                            choices=["데이터베이스", "Excel/CSV 파일"],
                            value="데이터베이스",
                            label="데이터 소스 유형"
                        )
                        
                        # 데이터베이스 연결 선택
                        with gr.Group(visible=True) as db_group:
                            db_connection = gr.Dropdown(
                                choices=["PostgreSQL - 샘플 DB", "MySQL - 테스트 DB"],
                                value="PostgreSQL - 샘플 DB",
                                label="데이터베이스 연결"
                            )
                        
                        # 파일 업로드
                        with gr.Group(visible=False) as file_group:
                            file_upload = gr.File(
                                label="Excel/CSV 파일 업로드",
                                file_types=[".xlsx", ".xls", ".csv"],
                                file_count="single"
                            )
                    
                    # 분석 옵션
                    with gr.Group():
                        gr.Markdown("### ⚙️ 분석 옵션", elem_classes=["section-header"])
                        
                        with gr.Row():
                            auto_visualize = gr.Checkbox(
                                label="자동 시각화",
                                value=True
                            )
                            include_insights = gr.Checkbox(
                                label="인사이트 분석",
                                value=True
                            )
                        
                        chart_type = gr.Dropdown(
                            choices=["자동 선택", "막대 차트", "선 차트", "파이 차트", "산점도", "히스토그램"],
                            value="자동 선택",
                            label="선호 차트 유형"
                        )
                    
                    # 분석 시작 버튼
                    analyze_btn = gr.Button(
                        "🚀 분석 시작",
                        variant="primary",
                        size="lg"
                    )
                
                # 오른쪽 컬럼 - 질문 이력
                with gr.Column(scale=1):
                    gr.Markdown("### 📜 최근 질문", elem_classes=["section-header"])
                    
                    history_display = gr.HTML(
                        self.history_service.get_history_html()
                    )
                    
                    # 즐겨찾기
                    gr.Markdown("### ⭐ 즐겨찾기", elem_classes=["section-header"])
                    favorites_list = gr.HTML("""
                    <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem;">
                        <p style="margin: 0;"><strong>월별 매출 대시보드</strong></p>
                    </div>
                    """)
            
            # 결과 표시 영역
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📊 분석 결과", elem_classes=["section-header"])
                    
                    # 상태 표시
                    status_display = gr.HTML(visible=False)
                    
                    # 탭으로 결과 구성
                    with gr.Tabs():
                        
                        # 인사이트 탭
                        with gr.TabItem("💡 인사이트"):
                            insights_output = gr.Markdown(
                                "분석을 시작하려면 위에서 질문을 입력하고 '분석 시작' 버튼을 클릭하세요.",
                                elem_classes=["result-card"]
                            )
                        
                        # 시각화 탭
                        with gr.TabItem("📈 시각화"):
                            chart_output = gr.Plot(
                                label="차트"
                            )
                        
                        # 데이터 탭
                        with gr.TabItem("📋 상세 데이터"):
                            data_output = gr.Dataframe(
                                label="데이터 테이블",
                                interactive=False
                            )
                        
                        # SQL 쿼리 탭
                        with gr.TabItem("🔍 생성된 쿼리"):
                            sql_output = gr.Code(
                                label="실행된 SQL 쿼리",
                                language="python"  # sql이 지원되지 않으므로 python 사용
                            )
            
            # 이벤트 바인딩
            
            # 예시 질문 버튼 클릭
            example_btn1.click(
                lambda: "지난 3개월 월별 매출 현황을 차트로 보여주세요",
                outputs=question_input
            )
            example_btn2.click(
                lambda: "전년 대비 매출 성장률을 분석해주세요",
                outputs=question_input
            )
            example_btn3.click(
                lambda: "고객을 구매 패턴별로 세분화해주세요",
                outputs=question_input
            )
            
            # 데이터 소스 유형 변경
            def toggle_data_source(source_type):
                if source_type == "데이터베이스":
                    return gr.update(visible=True), gr.update(visible=False)
                else:
                    return gr.update(visible=False), gr.update(visible=True)
            
            data_source_type.change(
                toggle_data_source,
                inputs=data_source_type,
                outputs=[db_group, file_group]
            )
            
            # 분석 시작 버튼 클릭
            analyze_btn.click(
                self.process_question,
                inputs=[
                    question_input,
                    data_source_type,
                    db_connection,
                    file_upload,
                    auto_visualize,
                    include_insights,
                    chart_type,
                    session_state
                ],
                outputs=[
                    status_display,
                    insights_output,
                    chart_output,
                    data_output,
                    sql_output,
                    history_display,
                    session_state
                ]
            )
        
        return app
    
    def process_question(
        self,
        question: str,
        data_source_type: str,
        db_connection: str,
        file_upload: Optional[str],
        auto_visualize: bool,
        include_insights: bool,
        chart_type: str,
        session_state: Dict
    ) -> Tuple[gr.HTML, str, go.Figure, pd.DataFrame, str, str, Dict]:
        """질문 처리 및 분석 수행"""
        
        if not question.strip():
            return (
                gr.HTML("<div class='status-error'>❌ 질문을 입력해주세요.</div>", visible=True),
                "질문을 입력해주세요.",
                None,
                pd.DataFrame(),
                "",
                self.history_service.get_history_html(),
                session_state
            )
        
        try:
            # 상태 업데이트
            status_html = gr.HTML(
                "<div class='status-processing'>🔄 분석 중... 잠시만 기다려주세요.</div>",
                visible=True
            )
            
            # 백엔드 API 호출 또는 데모 모드 실행
            if self.use_demo_mode:
                insights, chart, data, sql_query = self._process_with_demo(question, chart_type)
            else:
                # 동기 버전의 API 호출 사용 (Gradio는 동기 함수만 지원)
                insights, chart, data, sql_query = self._process_with_api_sync(
                    question, data_source_type, db_connection, file_upload, 
                    auto_visualize, include_insights, chart_type
                )
            
            # 세션 기록 업데이트
            session_state["last_question"] = question
            session_state["last_result"] = {
                "insights": insights,
                "chart": chart,
                "data": data,
                "sql": sql_query,
                "timestamp": datetime.now().isoformat()
            }
            
            return (
                gr.HTML("<div class='status-success'>✅ 분석 완료!</div>", visible=True),
                insights,
                chart,
                data,
                sql_query,
                self.history_service.get_history_html(),
                session_state
            )
            
        except Exception as e:
            return (
                gr.HTML(f"<div class='status-error'>❌ 분석 중 오류가 발생했습니다: {str(e)}</div>", visible=True),
                f"오류가 발생했습니다: {str(e)}",
                None,
                pd.DataFrame(),
                "",
                self.history_service.get_history_html(),
                session_state
            )
    
    def _process_with_demo(
        self,
        question: str,
        chart_type: str
    ) -> Tuple[str, go.Figure, pd.DataFrame, str]:
        """데모 모드로 분석 처리"""
        
        # 데모 데이터 생성
        data, sql_query = self.demo_service.generate_sales_data(question)
        
        # 차트 생성
        chart = self.demo_service.generate_chart(data, chart_type)
        
        # 인사이트 생성
        insights = self.demo_service.generate_insights(question, data)
        
        # 이력에 추가
        self.history_service.add_question(question, True, {
            "data_rows": len(data),
            "chart_type": chart_type,
            "demo_mode": True
        })
        
        return insights, chart, data, sql_query
    
    def _process_with_api_sync(
        self,
        question: str,
        data_source_type: str,
        db_connection: str,
        file_upload: Optional[str],
        auto_visualize: bool,
        include_insights: bool,
        chart_type: str
    ) -> Tuple[str, go.Figure, pd.DataFrame, str]:
        """동기 버전의 API 호출 (Gradio용)"""
        
        options = {
            "auto_visualize": auto_visualize,
            "include_insights": include_insights,
            "chart_type": chart_type
        }
        
        # 동기 버전의 API 호출
        result = self.api_service.sync_execute_analysis(
            question=question,
            data_source_type=data_source_type.lower(),
            connection_id="default",
            options=options
        )
        
        if result["success"]:
            api_data = result["data"]
            
            # API 응답을 파싱하여 UI에 맞게 변환
            insights = self._parse_insights(api_data)
            chart = self._parse_chart(api_data)
            data = self._parse_data_table(api_data)
            sql_query = api_data.get("executed_sql", "")
            
            # 이력에 추가
            self.history_service.add_question(question, True, {
                "api_response": True,
                "execution_time": api_data.get("execution_time_ms", 0)
            })
            
            return insights, chart, data, sql_query
        else:
            # API 실패시 에러 메시지
            error_msg = result.get("error", "Unknown error")
            self.history_service.add_question(question, False, {"error": error_msg})
            
            # 빈 결과 반환
            return f"❌ API 오류: {error_msg}", go.Figure(), pd.DataFrame(), ""
    
    async def _process_with_api(
        self,
        question: str,
        data_source_type: str,
        db_connection: str,
        file_upload: Optional[str],
        auto_visualize: bool,
        include_insights: bool,
        chart_type: str
    ) -> Tuple[str, go.Figure, pd.DataFrame, str]:
        """실제 백엔드 API로 분석 처리"""
        
        options = {
            "auto_visualize": auto_visualize,
            "include_insights": include_insights,
            "chart_type": chart_type
        }
        
        # API 호출
        result = await self.api_service.execute_analysis(
            question=question,
            data_source_type=data_source_type.lower(),
            connection_id="default",  # 임시로 기본 연결 사용
            options=options
        )
        
        if result["success"]:
            api_data = result["data"]
            
            # API 응답을 파싱하여 UI에 맞게 변환
            insights = self._parse_insights(api_data)
            chart = self._parse_chart(api_data)
            data = self._parse_data_table(api_data)
            sql_query = api_data.get("executed_sql", "")
            
            # 이력에 추가
            self.history_service.add_question(question, True, {
                "api_response": True,
                "execution_time": api_data.get("execution_time_ms", 0)
            })
            
            return insights, chart, data, sql_query
        else:
            # API 실패시 에러 메시지
            error_msg = result.get("error", "Unknown error")
            self.history_service.add_question(question, False, {"error": error_msg})
            
            # 빈 결과 반환
            return f"❌ API 오류: {error_msg}", go.Figure(), pd.DataFrame(), ""
    
    def _parse_insights(self, api_data: Dict[str, Any]) -> str:
        """API 응답에서 인사이트 파싱"""
        insights = api_data.get("insights", {})
        if isinstance(insights, dict):
            summary = insights.get("summary", "")
            findings = insights.get("key_findings", [])
            recommendations = insights.get("recommendations", [])
            
            result = f"## 📊 분석 결과\n\n{summary}\n\n"
            
            if findings:
                result += "### 🔍 주요 발견사항\n"
                for finding in findings:
                    result += f"- {finding}\n"
                result += "\n"
            
            if recommendations:
                result += "### 💡 권장사항\n"
                for i, rec in enumerate(recommendations, 1):
                    result += f"{i}. {rec}\n"
            
            return result
        else:
            return str(insights)
    
    def _parse_chart(self, api_data: Dict[str, Any]) -> go.Figure:
        """API 응답에서 차트 파싱"""
        visualizations = api_data.get("visualizations", [])
        
        if visualizations and len(visualizations) > 0:
            # 첫 번째 시각화 사용
            viz = visualizations[0]
            chart_data = viz.get("chart_data", {})
            
            # Plotly JSON에서 Figure 생성
            try:
                return go.Figure(chart_data)
            except Exception:
                # 파싱 실패시 빈 차트
                return go.Figure()
        
        return go.Figure()
    
    def _parse_data_table(self, api_data: Dict[str, Any]) -> pd.DataFrame:
        """API 응답에서 데이터 테이블 파싱"""
        data = api_data.get("data", {})
        
        if isinstance(data, dict):
            columns = data.get("columns", [])
            rows = data.get("rows", [])
            
            if columns and rows:
                return pd.DataFrame(rows, columns=columns)
        
        return pd.DataFrame()


def create_app() -> gr.Blocks:
    """Gradio 앱 생성"""
    ui = DataGenieUI()
    return ui.setup_interface()


if __name__ == "__main__":
    # 개발 모드에서 직접 실행
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
