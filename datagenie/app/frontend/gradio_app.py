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
        
        # 🎨 Modern & Simple Design System - 모던하고 심플한 디자인
        custom_css = """
        /* === MODERN MINIMALIST DESIGN SYSTEM === */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
        
        :root {
            /* 🎨 심플한 모던 컬러 팔레트 */
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --primary-light: #8b5cf6;
            --secondary: #64748b;
            --accent: #0ea5e9;
            --success: #059669;
            --warning: #d97706;
            --error: #dc2626;
            
            /* 🌫️ 중성 컬러 시스템 - 더 진한 색상으로 가독성 개선 */
            --gray-50: #f8fafc;
            --gray-100: #f1f5f9;
            --gray-200: #e2e8f0;
            --gray-300: #cbd5e1;
            --gray-400: #64748b;    /* 더 진하게 */
            --gray-500: #475569;    /* 더 진하게 */
            --gray-600: #334155;    /* 더 진하게 */
            --gray-700: #1e293b;    /* 더 진하게 */
            --gray-800: #0f172a;    /* 더 진하게 */
            --gray-900: #000000;    /* 완전한 검은색으로 */
            
            /* ✨ 서브틀 글래스 효과 */
            --glass-bg: rgba(255, 255, 255, 0.95);
            --glass-border: rgba(226, 232, 240, 0.8);
            --glass-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
            --glass-backdrop: blur(12px) saturate(120%);
            
            /* 📱 가독성 중심 타이포그래피 */
            --font-display: 'SF Pro Display', 'Inter', system-ui, -apple-system, sans-serif;
            --font-body: 'Inter', system-ui, -apple-system, sans-serif;
            --font-mono: 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
            
            /* 🎯 통일된 폰트 크기 시스템 */
            --font-size-base: 16px;    /* 기본 폰트 크기 */
            --font-size-large: 20px;   /* 큰 텍스트 (헤더 부제목, 섹션 제목) */
            --font-size-xlarge: 32px;  /* 메인 헤더 제목 */
            
            /* 📐 정교한 간격 시스템 */
            --space-0: 0;
            --space-1: 0.25rem;   /* 4px */
            --space-2: 0.5rem;    /* 8px */
            --space-3: 0.75rem;   /* 12px */
            --space-4: 1rem;      /* 16px */
            --space-5: 1.25rem;   /* 20px */
            --space-6: 1.5rem;    /* 24px */
            --space-8: 2rem;      /* 32px */
            --space-10: 2.5rem;   /* 40px */
            --space-12: 3rem;     /* 48px */
            --space-16: 4rem;     /* 64px */
            --space-20: 5rem;     /* 80px */
            --space-24: 6rem;     /* 96px */
            
            /* 🌈 프리미엄 그라데이션 세트 */
            --gradient-hero: linear-gradient(135deg, 
                #667eea 0%, 
                #764ba2 25%, 
                #f093fb 50%, 
                #f5576c 75%, 
                #4facfe 100%);
            --gradient-card: linear-gradient(145deg, 
                rgba(255, 255, 255, 0.9) 0%, 
                rgba(255, 255, 255, 0.7) 50%, 
                rgba(255, 255, 255, 0.85) 100%);
            --gradient-button: linear-gradient(135deg, 
                #667eea 0%, 
                #764ba2 50%, 
                #f093fb 100%);
            --gradient-text: linear-gradient(135deg, 
                #667eea 0%, 
                #764ba2 50%, 
                #f093fb 100%);
                
            /* 🔮 프리미엄 박스 섀도우 시스템 */
            --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04);
            --shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.15);
            --shadow-glow: 0 0 20px rgba(102, 126, 234, 0.4);
            --shadow-neon: 0 0 30px rgba(102, 126, 234, 0.6);
            
            /* 🎬 애니메이션 이징 */
            --ease-out-cubic: cubic-bezier(0.215, 0.61, 0.355, 1);
            --ease-in-out-cubic: cubic-bezier(0.645, 0.045, 0.355, 1);
            --ease-spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
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
        
        /* === 🌫️ 모던 심플 컨테이너 === */
        .gradio-container {
            max-width: 1200px !important;
            width: 100% !important;
            margin: 0 auto !important;
            background: 
                /* 🎨 서브틀 그라데이션 */
                linear-gradient(135deg, var(--gray-50) 0%, var(--gray-100) 100%);
            min-height: 100vh !important;
            padding: var(--space-6) var(--space-8) !important;
            position: relative !important;
            font-family: var(--font-body) !important;
            box-sizing: border-box !important;
        }
        
        /* === 미니멀 장식 요소 === */
        .gradio-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, 
                transparent 0%, 
                var(--primary) 50%, 
                transparent 100%);
            opacity: 0.3;
        }
        
        /* === 메인 콘텐츠 컨테이너 === */
        .gradio-container > * {
            position: relative;
            z-index: 1;
        }
        
        /* === 🌟 모던 심플 헤더 === */
        .main-header {
            background: white;
            border: 1px solid var(--gray-200);
            color: var(--gray-900);
            padding: var(--space-8) var(--space-6);
            border-radius: 16px;
            margin-bottom: var(--space-6);
            box-shadow: var(--glass-shadow);
            position: relative;
            transition: all 0.3s ease;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }
        
        .main-header:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            border-color: var(--primary);
        }
        
        /* 헤더 텍스트 가독성 최적화 */
        
        /* === 🌟 모던 심플 헤더 텍스트 === */
        .main-header h1 {
            font-family: var(--font-display) !important;
            font-size: var(--font-size-xlarge) !important;
            font-weight: 700 !important;
            margin: 0 !important;
            color: var(--gray-900) !important;
            letter-spacing: -0.025em;
            line-height: 1.1;
            position: relative;
            z-index: 2;
        }
        
        /* 헤더 부제목 */
        .main-header p {
            font-size: var(--font-size-large) !important;
            margin: var(--space-3) 0 0 0 !important;
            color: var(--gray-600) !important;
            font-weight: 400;
            letter-spacing: 0.01em;
            line-height: 1.5;
        }
        
        /* === 🌟 모던 심플 카드 시스템 === */
        .gr-box, .gr-form, .gr-panel {
            background: white !important;
            border: 1px solid var(--gray-200) !important;
            border-radius: 12px !important;
            box-shadow: var(--glass-shadow) !important;
            margin: var(--space-5) 0 !important;
            padding: var(--space-6) !important;
            transition: all 0.2s ease !important;
            position: relative !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        
        /* 심플한 호버 효과 */
        .gr-box:hover, .gr-form:hover, .gr-panel:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08) !important;
            border-color: var(--gray-300) !important;
        }
        
        /* 포커스 상태 */
        .gr-box:focus-within, .gr-form:focus-within, .gr-panel:focus-within {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }
        
        /* 모던 입력 필드 - 가독성 개선 */
        .gr-textbox, .gr-textarea {
            border: 1px solid var(--gray-300) !important;
            border-radius: 8px !important;
            font-size: var(--font-size-base) !important;
            padding: var(--space-4) var(--space-4) !important;
            background: white !important;
            color: var(--gray-900) !important;
            font-weight: 500 !important;
            line-height: 1.5 !important;
            transition: all 0.2s ease !important;
            font-family: var(--font-body) !important;
        }
        
        .gr-textbox:focus, .gr-textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
            outline: none !important;
        }
        
        .gr-textbox::placeholder, .gr-textarea::placeholder {
            color: var(--gray-500) !important;
            font-weight: 400 !important;
        }
        
        /* === 🌟 모던 심플 버튼 시스템 === */
        .gr-button {
            background: var(--primary) !important;
            border: 1px solid var(--primary) !important;
            border-radius: 8px !important;
            color: white !important;
            font-family: var(--font-body) !important;
            font-weight: 500 !important;
            font-size: var(--font-size-base) !important;
            padding: var(--space-4) var(--space-8) !important;
            transition: all 0.2s ease !important;
            text-transform: none !important;
            position: relative !important;
            cursor: pointer !important;
        }
        
        .gr-button:hover {
            background: var(--primary-hover) !important;
            border-color: var(--primary-hover) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
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
        
        /* 라벨 및 텍스트 - 더 진한 색상으로 가독성 개선 */
        .gr-form label, .gr-box label {
            color: var(--gray-900) !important;
            font-weight: 600 !important;
            font-size: var(--font-size-base) !important;
            margin-bottom: var(--space-2) !important;
            margin-top: 0 !important;
            font-family: var(--font-body) !important;
            display: block !important;
        }
        
        /* 라벨과 입력 필드 사이 간격 조정 */
        .gr-form label + .gr-textbox,
        .gr-form label + .gr-textarea,
        .gr-form label + .gr-dropdown,
        .gr-form label + .gr-checkbox-group,
        .gr-form label + .gr-radio-group,
        .gr-box label + .gr-textbox,
        .gr-box label + .gr-textarea,
        .gr-box label + .gr-dropdown,
        .gr-box label + .gr-checkbox-group,
        .gr-box label + .gr-radio-group {
            margin-top: var(--space-1) !important;
        }
        
        /* 심플한 섹션 헤더 */
        .section-header {
            margin: var(--space-6) 0 var(--space-4) 0 !important;
            padding: 0 !important;
            background: none !important;
            border: none !important;
        }
        
        .section-header h3 {
            color: var(--gray-900) !important;
            font-weight: 600 !important;
            font-size: var(--font-size-large) !important;
            margin: 0 !important;
            font-family: var(--font-display) !important;
        }
        
        .gr-markdown {
            color: var(--gray-900) !important;
            line-height: 1.6 !important;
            font-family: var(--font-body) !important;
            font-size: var(--font-size-base) !important;
        }
        
        .gr-markdown h1, .gr-markdown h2, .gr-markdown h3 {
            color: var(--gray-900) !important;
            font-weight: 600 !important;
            margin: var(--space-4) 0 var(--space-3) 0 !important;
            font-family: var(--font-display) !important;
        }
        
        .gr-markdown h1 { font-size: var(--font-size-large) !important; }
        .gr-markdown h2 { font-size: var(--font-size-large) !important; }
        .gr-markdown h3 { font-size: var(--font-size-large) !important; }
        
        /* 심플한 상태 표시 */
        .status-success {
            background: var(--success);
            color: white !important;
            padding: var(--space-3) var(--space-4);
            border-radius: 8px;
            font-weight: 500 !important;
            font-size: var(--font-size-base) !important;
            border: 1px solid var(--success);
        }
        
        .status-error {
            background: var(--error);
            color: white !important;
            padding: var(--space-3) var(--space-4);
            border-radius: 8px;
            font-weight: 500 !important;
            font-size: var(--font-size-base) !important;
            border: 1px solid var(--error);
        }
        
        .status-processing {
            background: var(--warning);
            color: white !important;
            padding: var(--space-3) var(--space-4);
            border-radius: 8px;
            font-weight: 500 !important;
            font-size: var(--font-size-base) !important;
            border: 1px solid var(--warning);
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
            color: #000000 !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
            display: block !important;
            margin-bottom: 0.5rem !important;
        }
        
        .history-item small {
            color: #334155 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
        }
        
        /* 데이터 테이블 */
        .gr-dataframe {
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }
        
        .gr-dataframe table {
            font-size: 14px !important;
            color: #000000 !important;
            font-weight: 500 !important;
        }
        
        .gr-dataframe th {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
            color: #000000 !important;
            font-weight: 700 !important;
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
            color: #ffffff !important;
            font-family: 'Fira Code', 'Monaco', 'Consolas', monospace !important;
            font-size: 14px !important;
            font-weight: 500 !important;
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
        
        /* 반응형 디자인 개선 */
        @media (max-width: 1200px) {
            .gradio-container {
                max-width: 95% !important;
                padding: var(--space-3) var(--space-4) !important;
            }
        }
        
        @media (max-width: 768px) {
            .gradio-container {
                max-width: 100% !important;
                padding: var(--space-2) var(--space-3) !important;
            }
            
            .main-header {
                padding: var(--space-4) var(--space-4) !important;
                margin-bottom: var(--space-3) !important;
            }
            
            .main-header h1 {
                font-size: var(--font-size-large) !important;
            }
            
            .main-header p {
                font-size: var(--font-size-base) !important;
            }
            
            .gr-box, .gr-form, .gr-panel {
                padding: var(--space-3) !important;
                margin: var(--space-2) 0 !important;
            }
        }
        
        /* 전체 페이지 레이아웃 개선 */
        body {
            margin: 0 !important;
            padding: 0 !important;
            background: var(--gray-50) !important;
            font-size: var(--font-size-base) !important;
            font-family: var(--font-body) !important;
        }
        
        /* 모든 텍스트 요소에 일관된 폰트 크기 적용 */
        *, *::before, *::after {
            font-size: inherit !important;
        }
        
        /* Gradio 기본 텍스트 요소들 */
        .gr-textbox, .gr-textarea, .gr-button, .gr-markdown, 
        .gr-label, .gr-form label, .gr-box label, 
        .gr-radio, .gr-checkbox, .gr-dropdown,
        .gr-file, .gr-upload, .gr-slider,
        p, span, div:not(.main-header):not(.section-header) {
            font-size: var(--font-size-base) !important;
            font-family: var(--font-body) !important;
        }
        
        /* === 📦 카드 내부 요소 간격 통일 === */
        .gr-box > *, .gr-form > *, .gr-panel > * {
            margin-bottom: var(--space-4) !important;
        }
        
        .gr-box > *:last-child, .gr-form > *:last-child, .gr-panel > *:last-child {
            margin-bottom: 0 !important;
        }
        
        /* 카드 내부 입력 요소들 간격 */
        .gr-box .gr-textbox, .gr-box .gr-textarea, .gr-box .gr-dropdown,
        .gr-form .gr-textbox, .gr-form .gr-textarea, .gr-form .gr-dropdown,
        .gr-panel .gr-textbox, .gr-panel .gr-textarea, .gr-panel .gr-dropdown {
            margin-bottom: var(--space-4) !important;
        }
        
        /* 카드 내부 체크박스/라디오 그룹 간격 */
        .gr-box .gr-checkbox-group, .gr-box .gr-radio-group,
        .gr-form .gr-checkbox-group, .gr-form .gr-radio-group,
        .gr-panel .gr-checkbox-group, .gr-panel .gr-radio-group {
            margin-bottom: var(--space-4) !important;
        }
        
        /* 카드 내부 개별 체크박스/라디오 간격 */
        .gr-checkbox, .gr-radio {
            margin-bottom: var(--space-2) !important;
        }
        
        /* 카드 내부 버튼 간격 */
        .gr-box .gr-button, .gr-form .gr-button, .gr-panel .gr-button {
            margin-top: var(--space-4) !important;
            margin-bottom: var(--space-2) !important;
        }
        
        /* === 🎯 특수 컴포넌트 간격 조정 === */
        /* 파일 업로드 컴포넌트 */
        .gr-file, .gr-upload {
            margin-bottom: var(--space-4) !important;
            padding: var(--space-3) !important;
        }
        
        /* 슬라이더 컴포넌트 */
        .gr-slider {
            margin: var(--space-3) 0 var(--space-4) 0 !important;
            padding: var(--space-2) 0 !important;
        }
        
        /* 데이터프레임/테이블 컴포넌트 */
        .gr-dataframe, .gr-table {
            margin: var(--space-4) 0 !important;
        }
        
        /* 이미지/비디오 컴포넌트 */
        .gr-image, .gr-video, .gr-audio {
            margin: var(--space-4) 0 !important;
        }
        
        /* 플롯/차트 컴포넌트 */
        .gr-plot, .gr-chart {
            margin: var(--space-4) 0 !important;
        }
        
        /* HTML/마크다운 컴포넌트 */
        .gr-html, .gr-markdown {
            margin: var(--space-3) 0 var(--space-4) 0 !important;
            padding: 0 !important;
        }
        
        /* 상태 메시지 컴포넌트 */
        .gr-info, .gr-warning, .gr-error {
            margin: var(--space-3) 0 !important;
            padding: var(--space-3) var(--space-4) !important;
        }
        
        #root {
            width: 100% !important;
            min-height: 100vh !important;
        }
        
        /* Gradio 특정 클래스 오버라이드 */
        .block {
            width: 100% !important;
        }
        
        .grid-wrap {
            gap: var(--space-3) !important;
        }
        
        .wrap {
            gap: var(--space-2) !important;
        }
        
        /* 컬럼 간격 조정 */
        .gr-row {
            gap: var(--space-6) !important;
        }
        
        .gr-column {
            flex: 1 !important;
            min-width: 0 !important;
        }
        
        /* === 📋 Gradio 그룹 및 컨테이너 내부 간격 === */
        .gr-group {
            padding: var(--space-4) !important;
            margin-bottom: var(--space-4) !important;
        }
        
        .gr-group > * {
            margin-bottom: var(--space-3) !important;
        }
        
        .gr-group > *:last-child {
            margin-bottom: 0 !important;
        }
        
        /* 탭 패널 내부 간격 */
        .gr-tab-panel {
            padding: var(--space-4) !important;
        }
        
        .gr-tab-panel > * {
            margin-bottom: var(--space-4) !important;
        }
        
        .gr-tab-panel > *:last-child {
            margin-bottom: 0 !important;
        }
        
        /* 아코디언 내부 간격 */
        .gr-accordion {
            margin-bottom: var(--space-4) !important;
        }
        
        .gr-accordion-body {
            padding: var(--space-4) !important;
        }
        
        .gr-accordion-body > * {
            margin-bottom: var(--space-3) !important;
        }
        
        .gr-accordion-body > *:last-child {
            margin-bottom: 0 !important;
        }
        
        /* === 🔧 중첩 여백 최적화 === */
        /* 카드 안의 그룹 중첩 여백 조정 */
        .gr-box .gr-group, .gr-form .gr-group, .gr-panel .gr-group {
            margin-bottom: var(--space-3) !important;
            padding: 0 !important;
            background: none !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* 그룹 안의 카드 중첩 여백 조정 */
        .gr-group .gr-box, .gr-group .gr-form, .gr-group .gr-panel {
            margin-bottom: var(--space-3) !important;
            padding: var(--space-4) !important;
        }
        
        /* 첫 번째와 마지막 요소 여백 최적화 */
        .gr-box > *:first-child, .gr-form > *:first-child, .gr-panel > *:first-child,
        .gr-group > *:first-child, .gr-tab-panel > *:first-child {
            margin-top: 0 !important;
        }
        
        /* 컴포넌트 간 일관된 수직 리듬 */
        .gr-box .gr-textbox + .gr-textbox,
        .gr-box .gr-textarea + .gr-textarea,
        .gr-box .gr-dropdown + .gr-dropdown,
        .gr-form .gr-textbox + .gr-textbox,
        .gr-form .gr-textarea + .gr-textarea,
        .gr-form .gr-dropdown + .gr-dropdown {
            margin-top: var(--space-3) !important;
        }
        """
        
        # 🌟 모던 심플 테마 - 가독성과 심플함 중심
        modern_simple_theme = gr.themes.Base(
            primary_hue=gr.themes.colors.violet,
            secondary_hue=gr.themes.colors.slate,
            neutral_hue=gr.themes.colors.slate,
            font=[
                gr.themes.GoogleFont("Inter"),
                "system-ui",
                "-apple-system",
                "sans-serif"
            ],
            text_size=gr.themes.sizes.text_sm,
            spacing_size=gr.themes.sizes.spacing_sm,
            radius_size=gr.themes.sizes.radius_sm
        ).set(
            # 🎨 심플한 컬러 시스템
            body_background_fill="#f8fafc",
            background_fill_primary="white",
            background_fill_secondary="#f8fafc",
            
            # ✨ 버튼 컬러
            button_primary_background_fill="#6366f1",
            button_primary_background_fill_hover="#4f46e5",
            button_primary_text_color="white",
            
            # 🌟 테두리 및 그림자
            border_color_primary="#e2e8f0",
            shadow_drop="0 4px 16px rgba(0, 0, 0, 0.04)",
        )

        with gr.Blocks(
            title="🧞‍♂️ DataGenie - AI 데이터 분석 비서",
            theme=modern_simple_theme,
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
            
            # 레이아웃 구조 개선
            with gr.Row():
                # 왼쪽 컬럼 - 질문 입력 및 설정
                with gr.Column(scale=3, min_width=400):
                    
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
                with gr.Column(scale=2, min_width=300):
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
