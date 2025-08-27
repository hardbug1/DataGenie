"""
DataGenie Gradio Web Interface - Completely New Design
완전히 새롭게 디자인된 DataGenie 웹 인터페이스
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
import time
import random

from .services import DataGenieAPIService, DemoDataService, HistoryService

# 백엔드 API 설정
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class DataGenieNewUI:
    """DataGenie 완전히 새로운 웹 인터페이스"""
    
    def __init__(self):
        """UI 초기화"""
        self.api_service = DataGenieAPIService(API_BASE_URL)
        self.demo_service = DemoDataService()
        self.history_service = HistoryService()
        self.use_demo_mode = True
        
    def setup_interface(self) -> gr.Blocks:
        """UX 중심의 새로운 Gradio 인터페이스 설정"""
        
        # 🎯 UX 최적화된 디자인 시스템
        ux_optimized_css = """
        /* DataGenie UX-First Design System */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            /* UX-focused Color System */
            --primary: #6366F1;
            --primary-hover: #4F46E5;
            --secondary: #10B981;
            --accent: #F59E0B;
            --success: #059669;
            --error: #DC2626;
            --warning: #D97706;
            
            /* Semantic Colors */
            --bg-primary: #FAFBFC;
            --bg-secondary: #F8FAFC;
            --surface: #FFFFFF;
            --surface-elevated: rgba(255, 255, 255, 0.98);
            
            /* Text Hierarchy */
            --text-primary: #1E293B;
            --text-secondary: #475569;
            --text-muted: #64748B;
            --text-disabled: #94A3B8;
            
            /* Spacing Scale */
            --space-1: 0.25rem;  /* 4px */
            --space-2: 0.5rem;   /* 8px */
            --space-3: 0.75rem;  /* 12px */
            --space-4: 1rem;     /* 16px */
            --space-5: 1.25rem;  /* 20px */
            --space-6: 1.5rem;   /* 24px */
            --space-8: 2rem;     /* 32px */
            --space-10: 2.5rem;  /* 40px */
            --space-12: 3rem;    /* 48px */
            
            /* Shadow System */
            --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
            --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
            
            /* Interactive States */
            --focus-ring: 0 0 0 3px rgba(99, 102, 241, 0.1);
            --transition-fast: 150ms ease;
            --transition-smooth: 300ms cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Reset & Base */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
            background: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            line-height: 1.6 !important;
            -webkit-font-smoothing: antialiased !important;
        }
        
        /* === 🎯 UX-First Layout === */
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
            padding: var(--space-6) var(--space-4) !important;
            background: transparent !important;
            min-height: 100vh !important;
        }
        
        /* Compact Header */
        .compact-header {
            background: var(--surface) !important;
            border-radius: 16px !important;
            padding: var(--space-6) var(--space-8) !important;
            margin-bottom: var(--space-8) !important;
            box-shadow: var(--shadow-sm) !important;
            border: 1px solid #E2E8F0 !important;
            text-align: center !important;
            position: relative !important;
        }
        
        .compact-header::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
            border-radius: 16px 16px 0 0;
        }
        
        .brand-title {
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            color: var(--primary) !important;
            margin-bottom: var(--space-2) !important;
            line-height: 1.2 !important;
        }
        
        .brand-subtitle {
            font-size: 1.125rem !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
        }
        
        /* === 📝 Main Question Input (Hero Section) === */
        .question-hero {
            background: var(--surface) !important;
            border-radius: 20px !important;
            padding: var(--space-10) var(--space-8) !important;
            margin-bottom: var(--space-8) !important;
            box-shadow: var(--shadow-lg) !important;
            border: 2px solid #E2E8F0 !important;
            text-align: center !important;
            transition: var(--transition-smooth) !important;
            position: relative !important;
        }
        
        .question-hero:focus-within {
            border-color: var(--primary) !important;
            box-shadow: var(--shadow-lg), var(--focus-ring) !important;
            transform: translateY(-2px) !important;
        }
        
        .question-label {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            margin-bottom: var(--space-6) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: var(--space-3) !important;
        }
        
        /* Enhanced Input Field */
        .main-question-input {
            font-size: 1.125rem !important;
            font-weight: 500 !important;
            padding: var(--space-6) var(--space-6) !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 16px !important;
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            transition: var(--transition-smooth) !important;
            min-height: 120px !important;
            resize: none !important;
        }
        
        .main-question-input:focus {
            border-color: var(--primary) !important;
            box-shadow: var(--focus-ring) !important;
            outline: none !important;
            background: var(--surface) !important;
        }
        
        .main-question-input::placeholder {
            color: var(--text-muted) !important;
            font-size: 1rem !important;
        }
        
        /* === 🚀 Primary Action Button === */
        .action-button-container {
            text-align: center !important;
            margin: var(--space-8) 0 !important;
        }
        
        .primary-action-btn {
            background: linear-gradient(135deg, var(--primary), var(--primary-hover)) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: var(--space-5) var(--space-12) !important;
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            box-shadow: var(--shadow-md) !important;
            transition: var(--transition-smooth) !important;
            cursor: pointer !important;
            min-width: 200px !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .primary-action-btn:hover {
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: var(--shadow-xl), 0 0 20px rgba(99, 102, 241, 0.4) !important;
        }
        
        .primary-action-btn:active {
            transform: translateY(-1px) scale(1.02) !important;
        }
        
        /* === ⚙️ Collapsible Settings === */
        .settings-section {
            background: var(--surface) !important;
            border-radius: 16px !important;
            margin-bottom: var(--space-8) !important;
            box-shadow: var(--shadow-sm) !important;
            border: 1px solid #E2E8F0 !important;
            overflow: hidden !important;
            transition: var(--transition-smooth) !important;
        }
        
        .settings-header {
            padding: var(--space-5) var(--space-6) !important;
            background: var(--bg-secondary) !important;
            border-bottom: 1px solid #E2E8F0 !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            transition: var(--transition-fast) !important;
        }
        
        .settings-header:hover {
            background: #F1F5F9 !important;
        }
        
        .settings-title {
            font-size: 1.125rem !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            display: flex !important;
            align-items: center !important;
            gap: var(--space-2) !important;
        }
        
        .settings-content {
            padding: var(--space-6) !important;
        }
        
        /* === 📊 Results Section === */
        .results-container {
            background: var(--surface) !important;
            border-radius: 20px !important;
            padding: var(--space-8) !important;
            margin-top: var(--space-8) !important;
            box-shadow: var(--shadow-lg) !important;
            border: 1px solid #E2E8F0 !important;
            opacity: 0 !important;
            transform: translateY(20px) !important;
            transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        
        .results-container.visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        
        .results-header {
            text-align: center !important;
            margin-bottom: var(--space-8) !important;
            padding-bottom: var(--space-6) !important;
            border-bottom: 2px solid #E2E8F0 !important;
        }
        
        .results-title {
            font-size: 1.875rem !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            margin-bottom: var(--space-2) !important;
        }
        
        /* === 📱 Sidebar === */
        .sidebar {
            background: var(--surface) !important;
            border-radius: 16px !important;
            padding: var(--space-6) !important;
            box-shadow: var(--shadow-sm) !important;
            border: 1px solid #E2E8F0 !important;
            height: fit-content !important;
            position: sticky !important;
            top: var(--space-6) !important;
        }
        
        .sidebar-section {
            margin-bottom: var(--space-8) !important;
        }
        
        .sidebar-section:last-child {
            margin-bottom: 0 !important;
        }
        
        .sidebar-title {
            font-size: 1.125rem !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            margin-bottom: var(--space-4) !important;
            display: flex !important;
            align-items: center !important;
            gap: var(--space-2) !important;
        }
        
        /* === 🎨 Enhanced Components === */
        .gr-textbox, .gr-textarea {
            background: var(--bg-secondary) !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: var(--space-4) !important;
            font-size: 1rem !important;
            color: var(--text-primary) !important;
            transition: var(--transition-fast) !important;
        }
        
        .gr-textbox:focus, .gr-textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: var(--focus-ring) !important;
            outline: none !important;
            background: var(--surface) !important;
        }
        
        .gr-button {
            border-radius: 12px !important;
            padding: var(--space-3) var(--space-6) !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            transition: var(--transition-fast) !important;
            border: 2px solid transparent !important;
            cursor: pointer !important;
        }
        
        .gr-button.gr-button-secondary {
            background: var(--surface) !important;
            color: var(--primary) !important;
            border-color: var(--primary) !important;
        }
        
        .gr-button.gr-button-secondary:hover {
            background: var(--primary) !important;
            color: white !important;
            transform: translateY(-1px) !important;
        }
        
        /* === 🎯 Quick Action Buttons === */
        .quick-action {
            background: var(--bg-secondary) !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: var(--space-4) !important;
            margin-bottom: var(--space-3) !important;
            cursor: pointer !important;
            transition: var(--transition-fast) !important;
            text-align: left !important;
            font-weight: 500 !important;
            color: var(--text-secondary) !important;
        }
        
        .quick-action:hover {
            border-color: var(--primary) !important;
            background: var(--surface) !important;
            color: var(--primary) !important;
            transform: translateX(4px) !important;
        }
        
        /* === 📊 Status & Progress === */
        .status-indicator {
            display: inline-flex !important;
            align-items: center !important;
            gap: var(--space-2) !important;
            padding: var(--space-3) var(--space-5) !important;
            border-radius: 50px !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            margin: var(--space-4) 0 !important;
        }
        
        .status-processing {
            background: var(--warning) !important;
            color: white !important;
            animation: pulse 2s infinite !important;
        }
        
        .status-success {
            background: var(--success) !important;
            color: white !important;
        }
        
        .status-error {
            background: var(--error) !important;
            color: white !important;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        /* === 🏷️ Progress Steps === */
        .progress-steps {
            display: flex !important;
            justify-content: center !important;
            margin: var(--space-8) 0 !important;
            gap: var(--space-6) !important;
        }
        
        .progress-step {
            display: flex !important;
            align-items: center !important;
            gap: var(--space-2) !important;
            padding: var(--space-2) var(--space-4) !important;
            background: #E2E8F0 !important;
            border-radius: 50px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: var(--text-muted) !important;
            transition: var(--transition-fast) !important;
        }
        
        .progress-step.active {
            background: var(--primary) !important;
            color: white !important;
        }
        
        .progress-step.completed {
            background: var(--success) !important;
            color: white !important;
        }
        
        /* === 📱 Responsive Design === */
        @media (max-width: 768px) {
            .gradio-container {
                padding: var(--space-4) var(--space-3) !important;
            }
            
            .brand-title {
                font-size: 2rem !important;
            }
            
            .question-hero {
                padding: var(--space-8) var(--space-6) !important;
            }
            
            .question-label {
                font-size: 1.25rem !important;
            }
            
            .main-question-input {
                font-size: 1rem !important;
                min-height: 100px !important;
            }
            
            .primary-action-btn {
                font-size: 1.125rem !important;
                padding: var(--space-4) var(--space-8) !important;
                min-width: 180px !important;
            }
            
            .sidebar {
                position: static !important;
                margin-top: var(--space-6) !important;
            }
        }
        
        /* === 🎪 Loading & Animations === */
        .loading-dots {
            display: inline-flex !important;
            gap: 4px !important;
        }
        
        .loading-dots span {
            width: 6px !important;
            height: 6px !important;
            border-radius: 50% !important;
            background: currentColor !important;
            animation: loading-bounce 1.4s ease-in-out infinite both !important;
        }
        
        .loading-dots span:nth-child(1) { animation-delay: -0.32s !important; }
        .loading-dots span:nth-child(2) { animation-delay: -0.16s !important; }
        
        @keyframes loading-bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        
        /* === ♿ Accessibility === */
        .sr-only {
            position: absolute !important;
            width: 1px !important;
            height: 1px !important;
            padding: 0 !important;
            margin: -1px !important;
            overflow: hidden !important;
            clip: rect(0, 0, 0, 0) !important;
            white-space: nowrap !important;
            border: 0 !important;
        }
        
        /* Focus indicators */
        *:focus {
            outline: 2px solid var(--primary) !important;
            outline-offset: 2px !important;
        }
        
        button:focus, input:focus, textarea:focus {
            outline: none !important;
        }
        """
        
        # 새로운 테마
        theme = gr.themes.Soft(
            primary_hue=gr.themes.colors.violet,
            secondary_hue=gr.themes.colors.emerald,
            neutral_hue=gr.themes.colors.slate,
            font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
        )
        
        with gr.Blocks(
            title="🧞‍♂️ DataGenie - UX Optimized AI Analytics",
            theme=theme,
            css=ux_optimized_css
        ) as app:
            
            # 상태 변수
            session_state = gr.State({})
            current_step = gr.State(1)
            
            # 🎯 Compact Header
            with gr.Row():
                gr.HTML("""
                <div class="compact-header">
                    <h1 class="brand-title">🧞‍♂️ DataGenie</h1>
                    <p class="brand-subtitle">AI 데이터 분석, 3초만에 시작하세요</p>
                </div>
                """)
            
            # 🏷️ Progress Steps
            with gr.Row():
                gr.HTML("""
                <div class="progress-steps">
                    <div class="progress-step active" id="step-1">
                        <span>1️⃣</span>
                        <span>질문 입력</span>
                    </div>
                    <div class="progress-step" id="step-2">
                        <span>2️⃣</span>
                        <span>설정</span>
                    </div>
                    <div class="progress-step" id="step-3">
                        <span>3️⃣</span>
                        <span>분석 완료</span>
                    </div>
                </div>
                """)
            
            # 📝 Main Question Input (Hero)
            with gr.Row():
                with gr.Column(scale=4):
                    with gr.Group(elem_classes=["question-hero"]):
                        gr.HTML('<div class="question-label">💬 무엇을 분석하고 싶으신가요?</div>')
                        
                        question_input = gr.Textbox(
                            label="",
                            placeholder="예: 지난 6개월 매출 현황과 성장 트렌드를 분석해주세요",
                            lines=3,
                            show_label=False,
                            elem_classes=["main-question-input"],
                            autofocus=True
                        )
                        
                        # Quick Examples Row
                        with gr.Row():
                            ex1_btn = gr.Button("📈 매출 현황 분석", elem_classes=["gr-button-secondary"], size="sm")
                            ex2_btn = gr.Button("👥 고객 세분화", elem_classes=["gr-button-secondary"], size="sm")
                            ex3_btn = gr.Button("🎯 KPI 대시보드", elem_classes=["gr-button-secondary"], size="sm")
                        
                        # 🚀 Primary Action Button
                        with gr.Row():
                            gr.HTML('<div class="action-button-container">')
                            analyze_btn = gr.Button(
                                "🚀 AI 분석 시작하기",
                                elem_classes=["primary-action-btn"],
                                size="lg",
                                variant="primary"
                            )
                            gr.HTML('</div>')
                
                # 📱 Sidebar
                with gr.Column(scale=1, elem_classes=["sidebar"]):
                    # Recent Analysis
                    with gr.Group(elem_classes=["sidebar-section"]):
                        gr.HTML('<div class="sidebar-title">📜 최근 분석</div>')
                        history_display = gr.HTML(self._get_compact_history())
                    
                    # Quick Templates
                    with gr.Group(elem_classes=["sidebar-section"]):
                        gr.HTML('<div class="sidebar-title">⚡ 빠른 템플릿</div>')
                        
                        template1_btn = gr.Button("📊 월간 리포트", elem_classes=["quick-action"], size="sm")
                        template2_btn = gr.Button("📈 성장률 분석", elem_classes=["quick-action"], size="sm")
                        template3_btn = gr.Button("💰 수익성 분석", elem_classes=["quick-action"], size="sm")
                        template4_btn = gr.Button("🔍 트렌드 분석", elem_classes=["quick-action"], size="sm")
            
            # ⚙️ Collapsible Settings
            with gr.Row():
                with gr.Column(scale=4):
                    with gr.Group(elem_classes=["settings-section"]):
                        # Settings Header (Collapsible)
                        settings_toggle = gr.HTML("""
                        <div class="settings-header" onclick="toggleSettings()">
                            <div class="settings-title">
                                <span>⚙️</span>
                                <span>고급 설정</span>
                            </div>
                            <span id="settings-arrow">▼</span>
                        </div>
                        """)
                        
                        # Settings Content (Initially Hidden)
                        with gr.Group(elem_classes=["settings-content"], visible=False) as settings_content:
                            with gr.Row():
                                with gr.Column():
                                    data_source = gr.Radio(
                                        choices=["📊 데이터베이스", "📄 파일 업로드"],
                                        value="📊 데이터베이스",
                                        label="데이터 소스"
                                    )
                                    
                                    # Database Options
                                    with gr.Group(visible=True) as db_group:
                                        db_choice = gr.Dropdown(
                                            choices=["🐘 PostgreSQL - 메인", "🐬 MySQL - 분석", "🗃️ SQLite - 로컬"],
                                            value="🐘 PostgreSQL - 메인",
                                            label="데이터베이스"
                                        )
                                    
                                    # File Upload
                                    with gr.Group(visible=False) as file_group:
                                        file_upload = gr.File(
                                            label="Excel/CSV 파일",
                                            file_types=[".xlsx", ".csv", ".json"]
                                        )
                                
                                with gr.Column():
                                    with gr.Row():
                                        auto_viz = gr.Checkbox(label="🎨 자동 시각화", value=True)
                                        ai_insights = gr.Checkbox(label="🧠 AI 인사이트", value=True)
                                    
                                    analysis_depth = gr.Slider(
                                        minimum=1, maximum=5, value=3, step=1,
                                        label="분석 깊이",
                                        info="1: 빠른 분석 ↔ 5: 심층 분석"
                                    )
                with gr.Column(scale=1):
                    pass  # Sidebar space
            
            # 📊 Results Section
            with gr.Row():
                with gr.Column():
                    # Status Display
                    status_display = gr.HTML(visible=False)
                    
                    # Results Container with Animation
                    with gr.Group(elem_classes=["results-container"], visible=False) as results_section:
                        with gr.Group(elem_classes=["results-header"]):
                            gr.HTML('<div class="results-title">🎯 분석 결과</div>')
                        
                        with gr.Tabs():
                            # AI Insights Tab
                            with gr.TabItem("💡 AI 인사이트"):
                                insights_output = gr.Markdown(
                                    """
                                    ## 🚀 분석을 시작해보세요!
                                    
                                    위에서 질문을 입력하고 **'AI 분석 시작하기'** 버튼을 클릭하면 
                                    AI가 데이터를 분석하여 인사이트를 제공합니다.
                                    
                                    ### 💡 예시 질문들:
                                    - "지난 6개월 매출 트렌드는 어떻게 되나요?"
                                    - "고객을 구매 패턴별로 분류해주세요"
                                    - "어떤 제품이 가장 수익성이 높은가요?"
                                    """
                                )
                            
                            # Visualization Tab
                            with gr.TabItem("📈 시각화"):
                                chart_output = gr.Plot(
                                    label="인터랙티브 차트"
                                )
                            
                            # Data Tab
                            with gr.TabItem("📋 데이터"):
                                data_output = gr.Dataframe(
                                    label="상세 데이터",
                                    interactive=True,
                                    wrap=True
                                )
                            
                            # Query Tab
                            with gr.TabItem("🔍 실행 코드"):
                                query_output = gr.Code(
                                    label="생성된 SQL/Python 코드",
                                    language="sql"
                                )
            
            # JavaScript for Settings Toggle
            gr.HTML("""
            <script>
            function toggleSettings() {
                const content = document.querySelector('.settings-content');
                const arrow = document.getElementById('settings-arrow');
                
                if (content.style.display === 'none' || !content.style.display) {
                    content.style.display = 'block';
                    arrow.textContent = '▲';
                } else {
                    content.style.display = 'none';
                    arrow.textContent = '▼';
                }
            }
            
            // Auto-focus on question input
            window.addEventListener('load', function() {
                const questionInput = document.querySelector('.main-question-input textarea');
                if (questionInput) {
                    questionInput.focus();
                }
            });
            </script>
            """)
            
            # Event Handlers
            
            # Example buttons
            ex1_btn.click(
                lambda: "지난 6개월간 매출 현황과 트렌드를 분석해주세요",
                outputs=question_input
            )
            ex2_btn.click(
                lambda: "고객을 구매 패턴별로 세분화하고 각 그룹의 특성을 분석해주세요",
                outputs=question_input
            )
            ex3_btn.click(
                lambda: "핵심 성과 지표(KPI)를 대시보드 형태로 보여주세요",
                outputs=question_input
            )
            
            # Template buttons
            template1_btn.click(
                lambda: "이번 달 전체 비즈니스 성과를 종합한 월간 리포트를 생성해주세요",
                outputs=question_input
            )
            template2_btn.click(
                lambda: "전년 동기 대비 성장률과 성장 동력을 분석해주세요",
                outputs=question_input
            )
            template3_btn.click(
                lambda: "제품별, 지역별 수익성을 분석하고 개선 방안을 제시해주세요",
                outputs=question_input
            )
            
            # Data source toggle
            def toggle_data_source(source):
                if source == "📊 데이터베이스":
                    return gr.update(visible=True), gr.update(visible=False)
                else:
                    return gr.update(visible=False), gr.update(visible=True)
            
            data_source.change(
                toggle_data_source,
                inputs=data_source,
                outputs=[db_group, file_group]
            )
            
            # Main analyze button
            analyze_btn.click(
                self.process_analysis,
                inputs=[
                    question_input, data_source, db_choice, file_upload,
                    auto_viz, ai_insights, analysis_depth, session_state
                ],
                outputs=[
                    status_display, results_section, insights_output,
                    chart_output, data_output, query_output, session_state
                ]
            )
        
        return app
    
    def process_analysis(self, question, data_source, db_choice, file_upload, 
                        auto_viz, ai_insights, depth, session_state):
        """UX 최적화된 분석 처리"""
        
        if not question.strip():
            return (
                gr.HTML('''
                <div class="status-indicator status-error">
                    ❌ 질문을 입력해주세요
                </div>
                ''', visible=True),
                gr.update(visible=False),
                "## ❌ 질문이 필요합니다\n\n분석을 위해 질문을 입력해주세요.",
                None, pd.DataFrame(), "", session_state
            )
        
        try:
            # Step 1: 질문 분석 중
            status_html = gr.HTML('''
            <div class="status-indicator status-processing">
                🔍 질문을 분석하는 중입니다
                <div class="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            ''', visible=True)
            
            time.sleep(1)
            
            # Step 2: 데이터 처리 중
            status_html = gr.HTML('''
            <div class="status-indicator status-processing">
                🔄 AI가 데이터를 분석하는 중입니다
                <div class="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            ''', visible=True)
            
            time.sleep(2)
            
            # Generate demo results
            insights, chart, data, query = self._generate_demo_results(question, depth)
            
            # Update session
            analysis_id = f"analysis_{int(time.time())}"
            session_state[analysis_id] = {
                "question": question,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "depth": depth
            }
            
            # Add to history
            self.history_service.add_question(question, True, {
                "analysis_id": analysis_id,
                "depth": depth,
                "data_source": data_source
            })
            
            return (
                gr.HTML('''
                <div class="status-indicator status-success">
                    ✅ 분석이 완료되었습니다!
                </div>
                ''', visible=True),
                gr.update(visible=True, elem_classes=["results-container", "visible"]),
                insights, chart, data, query, session_state
            )
            
        except Exception as e:
            return (
                gr.HTML(f'''
                <div class="status-indicator status-error">
                    ❌ 오류가 발생했습니다: {str(e)}
                </div>
                ''', visible=True),
                gr.update(visible=True),
                f"## ❌ 분석 오류\n\n{str(e)}\n\n다시 시도해주세요.",
                None, pd.DataFrame(), "", session_state
            )
    
    def _generate_demo_results(self, question, depth):
        """데모 결과 생성"""
        
        # Generate insights based on question type
        if "매출" in question or "revenue" in question.lower():
            insights = self._generate_sales_insights(depth)
            chart = self._create_sales_chart()
            data = self._create_sales_data()
            query = "SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as revenue FROM orders GROUP BY month;"
        
        elif "고객" in question or "customer" in question.lower():
            insights = self._generate_customer_insights(depth)
            chart = self._create_customer_chart()
            data = self._create_customer_data()
            query = "SELECT segment, COUNT(*) as customers, AVG(purchase_amount) as avg_purchase FROM customer_segments GROUP BY segment;"
        
        else:
            insights = self._generate_general_insights(depth)
            chart = self._create_general_chart()
            data = self._create_general_data()
            query = "SELECT category, value FROM analysis_data ORDER BY value DESC;"
        
        return insights, chart, data, query
    
    def _generate_sales_insights(self, depth):
        """매출 인사이트 생성"""
        base = """# 📈 매출 분석 결과

## 🔍 핵심 발견사항
- **총 매출**: 8.97억원 (전년 대비 +15.3%)
- **월평균 성장률**: 8.2%
- **최고 성장월**: 4월 (+23.1%)

## 💡 주요 인사이트
1. **꾸준한 상승세**: 6개월 연속 성장 기록
2. **계절성 효과**: 봄철 매출 증가 패턴 확인
3. **성장 동력**: 신규 고객 유입이 주요 동력

## 🎯 권장사항
- 4월 성공 요인을 다른 월에 적용
- 계절성을 활용한 마케팅 전략 수립
- 신규 고객 유입 채널 확대
"""
        
        if depth >= 4:
            base += """

## 🔬 심층 분석
### 📊 통계적 지표
- **변동계수**: 0.12 (안정적)
- **상관계수**: 0.89 (강한 양의 상관관계)
- **예측 신뢰도**: 94.2%

### 🎯 예측 결과
- **다음 달 예상 매출**: 1.85억원 (±5%)
- **분기 목표 달성률**: 103.7% 예상
"""
        
        return base
    
    def _generate_customer_insights(self, depth):
        """고객 인사이트 생성"""
        return """# 👥 고객 세분화 분석

## 🔍 고객 구성
- **총 고객수**: 12,450명
- **VIP 고객**: 8.3% (매출 기여도 42%)
- **신규 고객**: 23.7% (지속 증가 추세)

## 💡 세그먼트별 특성
1. **VIP 고객**: 높은 충성도, 프리미엄 제품 선호
2. **일반 고객**: 가격 민감, 프로모션 반응 높음
3. **신규 고객**: 첫 구매 후 재구매율 67%

## 🎯 마케팅 전략
- VIP 고객: 개인화된 프리미엄 서비스
- 일반 고객: 타겟 프로모션 강화
- 신규 고객: 온보딩 프로그램 개선
"""
    
    def _generate_general_insights(self, depth):
        """일반 인사이트 생성"""
        return """# 📊 데이터 분석 결과

## 🔍 분석 개요
데이터의 패턴과 트렌드를 종합적으로 분석했습니다.

## 💡 주요 발견사항
1. **데이터 분포**: 상위 20%가 전체의 80% 차지
2. **성장 패턴**: 지속적인 상승 추세
3. **변동성**: 안정적인 성장 패턴 유지

## 🎯 개선 방안
- 상위 항목의 성공 요인 분석
- 하위 항목의 개선 기회 발굴
- 데이터 기반 의사결정 강화
"""
    
    def _create_sales_chart(self):
        """매출 차트 생성"""
        months = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']
        revenue = [120, 135, 148, 182, 167, 195]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=revenue,
            mode='lines+markers',
            name='월별 매출',
            line=dict(color='#6366F1', width=3),
            marker=dict(size=10, color='#6366F1')
        ))
        
        fig.update_layout(
            title='📈 월별 매출 현황',
            xaxis_title='월',
            yaxis_title='매출 (백만원)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def _create_customer_chart(self):
        """고객 차트 생성"""
        segments = ['VIP', '일반', '신규', '휴면']
        counts = [1033, 6225, 2947, 2245]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=segments, y=counts,
            marker=dict(color=['#6366F1', '#10B981', '#F59E0B', '#EF4444'])
        ))
        
        fig.update_layout(
            title='👥 고객 세그먼트별 분포',
            xaxis_title='고객 세그먼트',
            yaxis_title='고객수',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def _create_general_chart(self):
        """일반 차트 생성"""
        categories = ['A', 'B', 'C', 'D', 'E']
        values = [45, 32, 28, 15, 12]
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=categories, values=values,
            hole=0.3,
            marker=dict(colors=['#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'])
        ))
        
        fig.update_layout(
            title='📊 카테고리별 분포',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def _create_sales_data(self):
        """매출 데이터 생성"""
        return pd.DataFrame({
            '월': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06'],
            '매출(백만원)': [120, 135, 148, 182, 167, 195],
            '성장률(%)': [0, 12.5, 9.6, 23.0, -8.2, 16.8],
            '목표대비(%)': [95.2, 102.3, 108.1, 121.3, 111.8, 118.5]
        })
    
    def _create_customer_data(self):
        """고객 데이터 생성"""
        return pd.DataFrame({
            '세그먼트': ['VIP', '일반', '신규', '휴면'],
            '고객수': [1033, 6225, 2947, 2245],
            '평균구매액(만원)': [45.2, 12.8, 8.3, 3.1],
            '재구매율(%)': [89.5, 67.2, 34.8, 12.1]
        })
    
    def _create_general_data(self):
        """일반 데이터 생성"""
        return pd.DataFrame({
            '카테고리': ['A', 'B', 'C', 'D', 'E'],
            '값': [450, 320, 280, 150, 120],
            '비율(%)': [33.6, 23.9, 20.9, 11.2, 9.0],
            '순위': [1, 2, 3, 4, 5]
        })
    
    def _get_compact_history(self):
        """컴팩트한 사이드바 이력 생성"""
        history_items = [
            {"q": "매출 분석", "time": "2분 전"},
            {"q": "고객 세분화", "time": "15분 전"},
            {"q": "ROI 분석", "time": "1시간 전"},
        ]
        
        html = ""
        for item in history_items:
            html += f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.5rem; cursor: pointer; transition: all 0.15s ease;">
                <div style="font-weight: 600; color: #1E293B; font-size: 0.875rem; margin-bottom: 0.25rem;">
                    {item['q']}
                </div>
                <div style="font-size: 0.75rem; color: #64748B;">
                    {item['time']}
                </div>
            </div>
            """
        
        return html if html else "<div style='text-align: center; color: #9CA3AF; padding: 1rem; font-size: 0.875rem;'>분석 이력이 없습니다</div>"
    
    def _get_demo_history(self):
        """데모 이력 생성"""
        history_items = [
            {"q": "매출 트렌드 분석", "time": "2분 전", "status": "완료"},
            {"q": "고객 세분화", "time": "15분 전", "status": "완료"},
            {"q": "제품 수익성", "time": "1시간 전", "status": "완료"},
        ]
        
        html = ""
        for item in history_items:
            html += f"""
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: #1F2937; margin-bottom: 0.25rem; font-size: 0.9rem;">
                    {item['q']}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <small style="color: #6B7280;">{item['time']}</small>
                    <span style="background: #10B981; color: white; padding: 0.25rem 0.5rem; border-radius: 6px; font-size: 0.75rem;">
                        {item['status']}
                    </span>
                </div>
            </div>
            """
        
        return html


def create_app() -> gr.Blocks:
    """새로운 Gradio 앱 생성"""
    ui = DataGenieNewUI()
    return ui.setup_interface()


if __name__ == "__main__":
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
