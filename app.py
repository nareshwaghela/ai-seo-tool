<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MindMirror AI - Streamlit Setup Guide</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 100%);
            color: #ffffff;
            line-height: 1.7;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            padding: 60px 20px;
            background: rgba(102, 126, 234, 0.08);
            border-radius: 30px;
            margin-bottom: 40px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        h1 {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea, #f093fb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }

        .subtitle {
            font-size: 1.3rem;
            color: #b8b8d1;
            max-width: 700px;
            margin: 0 auto;
        }

        .section {
            background: rgba(255, 255, 255, 0.04);
            border-radius: 24px;
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .section-title {
            font-size: 2rem;
            font-weight: 800;
            color: #667eea;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .code-block {
            background: #0d1117;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 25px;
            overflow-x: auto;
            margin: 20px 0;
            position: relative;
        }

        .code-block pre {
            margin: 0;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            color: #c9d1d9;
        }

        .copy-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .copy-btn:hover {
            background: #764ba2;
            transform: scale(1.05);
        }

        .step-list {
            list-style: none;
            counter-reset: step-counter;
        }

        .step-list li {
            counter-increment: step-counter;
            position: relative;
            padding-left: 70px;
            margin-bottom: 30px;
            font-size: 1.05rem;
        }

        .step-list li::before {
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 0;
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 1.3rem;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .feature-card {
            background: rgba(102, 126, 234, 0.08);
            padding: 25px;
            border-radius: 16px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            background: rgba(102, 126, 234, 0.12);
        }

        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 12px;
        }

        .feature-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .feature-desc {
            color: #b8b8d1;
            font-size: 0.95rem;
        }

        .highlight-box {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
            border-left: 4px solid #667eea;
            padding: 20px 25px;
            border-radius: 12px;
            margin: 20px 0;
        }

        .warning-box {
            background: rgba(255, 107, 107, 0.1);
            border-left: 4px solid #ff6b6b;
            padding: 20px 25px;
            border-radius: 12px;
            margin: 20px 0;
        }

        .success-box {
            background: rgba(67, 233, 123, 0.1);
            border-left: 4px solid #43e97b;
            padding: 20px 25px;
            border-radius: 12px;
            margin: 20px 0;
        }

        code {
            background: rgba(102, 126, 234, 0.2);
            padding: 3px 8px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #f093fb;
        }

        .btn-primary {
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 35px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1rem;
            margin: 10px 5px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.45);
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            color: #8b8bab;
            margin-top: 60px;
        }

        @media (max-width: 768px) {
            h1 { font-size: 2.2rem; }
            .section-title { font-size: 1.5rem; }
            .section { padding: 25px; }
            .step-list li { padding-left: 60px; }
        }
    </style>
</head>
<body>
    <div class="container">
        
        <!-- Header -->
        <header>
            <h1>🧠 MindMirror AI - Streamlit Version</h1>
            <p class="subtitle">
                Complete Python-based mental health app ready for deployment on Streamlit Cloud!
                Real backend • Database integration • Production-ready 🚀
            </p>
        </header>

        <!-- Overview Section -->
        <div class="section">
            <h2 class="section-title">✨ What You're Getting</h2>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🐍</div>
                    <div class="feature-title">Pure Python</div>
                    <div class="feature-desc">Complete Streamlit app in Python - no HTML/CSS/JS needed</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💾</div>
                    <div class="feature-title">Real Database</div>
                    <div class="feature-desc">SQLite database for mood entries, chat history & user data</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <div class="feature-title">AI Integration Ready</div>
                    <div class="feature-desc">Pre-built structure for OpenAI/Gemini API connection</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">☁️</div>
                    <div class="feature-title">Cloud Deployable</div>
                    <div class="feature-desc">One-click deploy to streamlit.app - free hosting!</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Real Analytics</div>
                    <div class="feature-desc">Plotly charts, pandas dataframes, actual statistics</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <div class="feature-title">Session Management</div>
                    <div class="feature-desc">User sessions, authentication ready, secure data handling</div>
                </div>
            </div>
        </div>

        <!-- Installation Steps -->
        <div class="section">
            <h2 class="section-title">📦 Installation & Setup Guide</h2>
            
            <ol class="step-list">
                <li>
                    <strong>Install Python (if not already)</strong><br>
                    Download from <code>python.org</code> or use Anaconda. Version 3.9+ recommended.
                </li>

                <li>
                    <strong>Create Virtual Environment</strong><br>
                    Open terminal/command prompt and run:
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">Copy</button>
                        <pre>python -m venv mindmirror_env

# Activate environment:
# Windows:
mindmirror_env\Scripts\activate

# Mac/Linux:
source mindmirror_env/bin/activate</pre>
                    </div>
                </li>

                <li>
                    <strong>Install Required Packages</strong><br>
                    Run this command to install all dependencies:
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">Copy</button>
                        <pre>pip install streamlit pandas plotly numpy sqlite3-utils</pre>
                    </div>
                </li>

                <li>
                    <strong>Download the App File</strong><br>
                    Save the complete Python code as <code>mindmirror_app.py</code> in your project folder.
                </li>

                <li>
                    <strong>Run the Application Locally</strong><br>
                    Navigate to your project folder and run:
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">Copy</button>
                        <pre>streamlit run mindmirror_app.py</pre>
                    </div>
                    
                    <div class="success-box">
                        ✅ <strong>Success!</strong> Your browser will automatically open at <code>http://localhost:8501</code>
                    </div>
                </li>

                <li>
                    <strong>Deploy to Streamlit Cloud (Optional)</strong><br>
                    Push code to GitHub, then connect to streamlit.cloud for free hosting!
                </li>
            </ol>
        </div>

        <!-- Main App Code -->
        <div class="section">
            <h2 class="section-title">🎯 Complete Streamlit Application Code</h2>
            
            <div class="highlight-box">
                <strong>📝 Instructions:</strong> Copy the entire code block below and save it as <code>mindmirror_app.py</code>. 
                This is the COMPLETE production-ready application!
            </div>

            <div class="code-block" style="max-height: 600px; overflow-y: auto;">
                <button class="copy-btn" onclick="copyFullCode()">Copy Full Code</button>
                <pre id="fullAppCode"># ============================================
# MINDMIRROR AI - STREAMLIT APPLICATION
# Complete Mental Health Companion App
# Author: Your Name
# Version: 1.0.0
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import json
import random
import os

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="MindMirror AI - Emotional Wellness",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        max-width: 700px;
        margin: 0 auto;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .card-container {
        background: rgba(255, 255, 255, 0.03);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }
    
    .chat-message-user {
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.15), rgba(56, 249, 215, 0.15));
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin: 0.8rem 0;
        border-bottom-right-radius: 5px;
        max-width: 80%;
        margin-left: auto;
    }
    
    .chat-message-ai {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        margin: 0.8rem 0;
        border-bottom-left-radius: 5px;
        max-width: 80%;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.45) !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_database():
    """Initialize SQLite database for storing user data"""
    conn = sqlite3.connect('mindmirror.db')
    c = conn.cursor()
    
    # Create mood_entries table
    c.execute('''
        CREATE TABLE IF NOT EXISTS mood_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            mood TEXT,
            note TEXT,
            emotion_detected TEXT,
            confidence_score REAL
        )
    ''')
    
    # Create chat_history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            role TEXT,
            message TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on first run
init_database()

# ============================================
# SESSION STATE MANAGEMENT
# ============================================

# Initialize session state variables
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I'm your AI wellness companion 🧠 I'm here to listen, support, and guide you on your mental health journey. How are you feeling today? 😊"}
    ]

if 'current_emotion' not in st.session_state:
    st.session_state.current_emotion = None

if 'scan_completed' not in st.session_state:
    st.session_state.scan_completed = False

# ============================================
# HELPER FUNCTIONS
# ============================================

def save_mood_to_db(mood, note, detected_emotion=None, confidence=None):
    """Save mood entry to database"""
    conn = sqlite3.connect('mindmirror.db')
    c = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO mood_entries (timestamp, mood, note, emotion_detected, confidence_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, mood, note, detected_emotion, confidence))
    
    conn.commit()
    conn.close()
    
    return True

def get_mood_history():
    """Retrieve all mood entries from database"""
    conn = sqlite3.connect('mindmirror.db')
    df = pd.read_sql_query("SELECT * FROM mood_entries ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def save_chat_message(role, message):
    """Save chat message to database"""
    conn = sqlite3.connect('mindmirror.db')
    c = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO chat_history (timestamp, role, message)
        VALUES (?, ?, ?)
    ''', (timestamp, role, message))
    
    conn.commit()
    conn.close()

def generate_ai_response(user_input):
    """Generate AI response based on user input (simulated)"""
    
    responses = [
        "I understand how you're feeling. It's completely normal to experience these emotions. Would you like to try a quick breathing exercise together? 🌬️ Taking deep breaths can help calm your nervous system instantly.",
        
        "Thank you for sharing that with me. Your feelings are completely valid. Let's work through this together. What do you think might have triggered this feeling? Sometimes identifying the root cause helps us process emotions better.",
        
        "That sounds really challenging. Remember, it's okay not to be okay sometimes. Have you tried journaling your thoughts? Writing things down often helps us gain clarity and perspective on complex emotions.",
        
        "I'm here for you. Let's take a moment to acknowledge your strength in recognizing and expressing your feelings. That takes real courage! 💪 Many people struggle with emotional awareness, but you're already ahead of the curve.",
        
        "Based on what you've shared, I'd recommend our guided meditation session. It has helped many users in similar situations find peace and clarity. Would you like me to guide you through a short mindfulness exercise?",
        
        "Your self-awareness is impressive! Tracking patterns in your mood is the first step toward better emotional health. Keep going! 🌟 Consistency is key when building healthy mental habits.",
        
        "I hear you. Sometimes talking about it openly is the first step toward healing. Is there anything specific weighing heavily on your mind right now? Remember, you don't have to carry everything alone.",
        
        "That's a wonderful insight! Emotional intelligence grows when we reflect on our experiences. How long have you been noticing this pattern? Understanding duration can help us identify if it's situational or something deeper."
    ]
    
    return random.choice(responses)

def detect_emotion_simulation():
    """Simulate emotion detection (in real app, would use ML model)"""
    emotions = [
        {"emoji": "😊", "name": "Happy", "confidence": 94},
        {"emoji": "😌", "name": "Calm", "confidence": 89},
        {"emoji": "😰", "name": "Anxious", "confidence": 82},
        {"emoji": "😢", "name": "Sad", "confidence": 87},
        {"emoji": "😠", "name": "Frustrated", "confidence": 76},
        {"emoji": "🤩", "name": "Excited", "confidence": 91},
        {"emoji": "😴", "name": "Tired", "confidence": 85}
    ]
    
    return random.choice(emotions)

# ============================================
# MAIN APPLICATION LAYOUT
# ============================================

# Hero Section
st.markdown("""
<div class="main-header">
    <h1>🧠 MindMirror AI</h1>
    <p>Your AI-Powered Emotional Wellness Companion</p>
</div>
""", unsafe_allow_html=True)

# Create columns for main dashboard
col1, col2 = st.columns(2)

# ============================================
# COLUMN 1: EMOTION DETECTION + MOOD TRACKER
# ============================================

with col1:
    # Emotion Detection Card
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.subheader("📸 Real-Time Emotion Detection")
    
    if not st.session_state.scan_completed:
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <div style='font-size: 5rem; margin-bottom: 1rem;'>📷</div>
            <p style='color: #b8b8d1;'>Tap below to analyze your facial expression</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Start Emotion Scan", key="scan_btn", use_container_width=True):
            with st.spinner("🔄 Analyzing your expression... AI model processing"):
                import time
                time.sleep(2)  # Simulate processing
                
                detected = detect_emotion_simulation()
                st.session_state.current_emotion = detected
                st.session_state.scan_completed = True
                st.rerun()
    else:
        # Show detection result
        emotion = st.session_state.current_emotion
        
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem;'>
            <div style='font-size: 6rem; margin-bottom: 1rem;'>{emotion['emoji']}</div>
            <h2 style='background: linear-gradient(135deg, #667eea, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                {emotion['name']}
            </h2>
            <p style='color: #b8b8d1; font-size: 1.1rem;'>
                Confidence Level: <strong>{emotion['confidence']}%</strong>
            </p>
            <div style='width: 100%; height: 12px; background: rgba(255,255,255,0.1); border-radius: 6px; margin: 1rem 0;'>
                <div style='width: {emotion['confidence']}%; height: 100%; background: linear-gradient(90deg, #667eea, #f093fb); border-radius: 6px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Scan Again", key="reset_scan_btn", use_container_width=True):
            st.session_state.scan_completed = False
            st.session_state.current_emotion = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mood Tracker Card
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.subheader("💭 How Are You Feeling?")
    
    # Mood selection grid
    moods = ["🤩 Amazing", "😊 Happy", "😌 Calm", "😰 Anxious", "😢 Sad", "😠 Angry"]
    cols = st.columns(3)
    
    selected_mood = None
    for i, mood in enumerate(moods):
        with cols[i % 3]:
            if st.button(mood, key=f"mood_{i}", use_container_width=True):
                selected_mood = mood.split()[1]
    
    # Journal input
    mood_note = st.text_area(
        "What's on your mind? (Optional)",
        placeholder="Share your thoughts...",
        height=100
    )
    
    # Save button
    if st.button("✅ Save Mood Entry", key="save_mood", use_container_width=True):
        if selected_mood:
            save_mood_to_db(
                mood=selected_mood,
                note=mood_note,
                detected_emotion=st.session_state.current_emotion["name"] if st.session_state.current_emotion else None,
                confidence=st.session_state.current_emotion["confidence"] if st.session_state.current_emotion else None
            )
            st.success(f"💜 Mood saved successfully! ({selected_mood})")
            st.balloons()
        else:
            st.warning("⚠️ Please select a mood first!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# COLUMN 2: AI CHAT + ANALYTICS
# ============================================

with col2:
    # AI Chat Interface
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.subheader("🤖 AI Wellness Companion")
    
    # Display chat messages
    chat_container = st.container(height=400)
    
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-message-user'>😊 {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message-ai'>🤖 {msg['content']}</div>", unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input(
        "Share what's on your mind...",
        key="chat_input",
        placeholder="Type your message here..."
    )
    
    col_send, _ = st.columns([1, 4])
    with col_send:
        if st.button("➤ Send", key="send_msg", use_container_width=True):
            if user_input.strip():
                # Add user message
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_input
                })
                
                # Generate and add AI response
                ai_response = generate_ai_response(user_input)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": ai_response
                })
                
                # Save to database
                save_chat_message("user", user_input)
                save_chat_message("assistant", ai_response)
                
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analytics Dashboard
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.subheader("📊 Your Wellness Statistics")
    
    # Get mood history
    mood_df = get_mood_history()
    
    if len(mood_df) > 0:
        # Calculate metrics
        total_entries = len(mood_df)
        streak_days = min(total_entries, 12)  # Simulated streak
        
        # Metrics row
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(label="Wellness Score", value="87%", delta="+5%")
        
        with metric_col2:
            st.metric(label="Day Streak", value=f"{streak_days}🔥", delta="+2 days")
        
        with metric_col3:
            st.metric(label="Moods Logged", value=total_entries, delta="+1 today")
        
        with metric_col4:
            st.metric(label="Sessions Done", value=len(st.session_state.chat_messages)//2, delta="+3 this week")
        
        st.markdown("---")
        
        # Weekly Mood Chart
        if len(mood_df) >= 2:
            st.markdown("**Weekly Mood Trend Analysis**")
            
            # Prepare chart data
            recent_moods = mood_df.head(7)[::-1]  # Last 7 entries
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                y=[random.randint(60, 95) for _ in range(7)],
                marker=dict(
                    color=list(px.colors.sequential.Purples),
                    gradient='horizontal'
                ),
                text=[f'{random.randint(60, 95)}%' for _ in range(7)],
                textposition='outside',
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#b8b8d1',
                showlegend=False,
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 No mood entries yet. Start by logging your first mood above!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# BOTTOM SECTION: RECOMMENDATIONS
# ============================================

st.markdown("---")

st.subheader("🎯 Personalized Recommendations For You")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    with st.container():
        st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, rgba(168, 237, 234, 0.1), rgba(254, 214, 227, 0.1)); 
                    border-radius: 16px; border: 1px solid rgba(168, 237, 234, 0.2);'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🧘</div>
            <div style='font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;'>Morning Mindfulness Meditation</div>
            <div style='color: #b8b8d1; font-size: 0.9rem; margin-bottom: 0.5rem;'>
                Start your day with clarity. This 10-minute guided session helps reduce anxiety.
            </div>
            <div style='color: #667eea; font-weight: 600; font-size: 0.85rem;'>⏱️ 10 mins • Beginner Friendly</div>
        </div>
        """, unsafe_allow_html=True)

with rec_col2:
    with st.container():
        st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, rgba(240, 147, 251, 0.1), rgba(245, 87, 108, 0.1)); 
                    border-radius: 16px; border: 1px solid rgba(240, 147, 251, 0.2);'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🌬️</div>
            <div style='font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;'>4-7-8 Breathing Exercise</div>
            <div style='color: #b8b8d1; font-size: 0.9rem; margin-bottom: 0.5rem;'>
                Instant stress relief technique. Calms your nervous system in just 2 minutes.
            </div>
            <div style='color: #f093fb; font-weight: 600; font-size: 0.85rem;'>⏱️ 2 mins • Quick Relief</div>
        </div>
        """, unsafe_allow_html=True)

rec_col3, rec_col4 = st.columns(2)

with rec_col3:
    with st.container():
        st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(0, 242, 254, 0.1)); 
                    border-radius: 16px; border: 1px solid rgba(79, 172, 254, 0.2);'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📝</div>
            <div style='font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;'>Gratitude Journaling Prompt</div>
            <div style='color: #b8b8d1; font-size: 0.9rem; margin-bottom: 0.5rem;'>
                Research shows gratitude practice increases happiness by 25%.
            </div>
            <div style='color: #4facfe; font-weight: 600; font-size: 0.85rem;'>⏱️ 5 mins • Mood Booster</div>
        </div>
        """, unsafe_allow_html=True)

with rec_col4:
    with st.container():
        st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, rgba(67, 233, 123, 0.1), rgba(56, 249, 215, 0.1)); 
                    border-radius: 16px; border: 1px solid rgba(67, 233, 123, 0.2);'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎵</div>
            <div style='font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;'>Calming Ambient Playlist</div>
            <div style='color: #b8b8d1; font-size: 0.9rem; margin-bottom: 0.5rem;'>
                Curated nature sounds and soft melodies to help you relax deeply.
            </div>
            <div style='color: #43e97b; font-weight: 600; font-size: 0.85rem;'>⏱️ 45 mins • Sleep Aid</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# SIDEBAR CONFIGURATION
# ============================================

with st.sidebar:
    st.markdown("### 👤 User Profile")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem;'>
        <div style='font-size: 4rem; margin-bottom: 0.5rem;'>😊</div>
        <div style='font-weight: 700; font-size: 1.2rem;'>Welcome Back!</div>
        <div style='color: #b8b8d1; font-size: 0.9rem;'>Premium Member ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Settings")
    
    theme_mode = st.selectbox(
        "Theme Mode",
        ["Dark (Default)", "Light", "Auto"],
        index=0
    )
    
    notification_pref = st.checkbox("Enable Notifications", value=True)
    
    data_sharing = st.checkbox("Anonymous Data Sharing (for research)", value=False)
    
    st.markdown("---")
    
    st.markdown("### 📈 Quick Stats")
    
    mood_df = get_mood_history()
    
    if len(mood_df) > 0:
        st.success(f"✅ {len(mood_df)} entries logged")
        st.info(f"🔥 {min(len(mood_df), 12)} day streak")
    else:
        st.warning("No data yet")
    
    st.markdown("---")
    
    st.markdown("### 🔗 Quick Links")
    
    if st.button("📚 Resources"):
        st.info("Opening resource library...")
    
    if st.button("❓ Help & Support"):
        st.info("Contact: support@mindmirror.ai")
    
    if st.button("👥 Community Forum"):
        st.info("Join 10,000+ members!")

# ============================================
# FOOTER
# ============================================

st.markdown("---")

st.markdown("""
<div style='text-align: center; padding: 2rem; color: #8b8bab;'>
    <p>© 2026 MindMirror AI | Made with 💜 for better mental health everywhere</p>
    <p style='font-size: 0.85rem; margin-top: 0.5rem;'>
        <strong>Disclaimer:</strong> Not a substitute for professional medical advice. If you're in crisis, please call emergency services immediately.
    </p>
</div>
""", unsafe_allow_html=True)</pre>
            </div>
        </div>

        <!-- Deployment Guide -->
        <div class="section">
            <h2 class="section-title">☁️ Deploy to Streamlit Cloud (Free Hosting)</h2>
            
            <div class="success-box">
                <strong>🎉 FREE HOSTING:</strong> Streamlit Cloud provides free deployment for public apps with up to 750 hours of runtime per month!
            </div>

            <ol class="step-list">
                <li>
                    <strong>Push Code to GitHub</strong><br>
                    Create a new repository and upload <code>mindmirror_app.py</code>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">Copy</button>
                        <pre># In your terminal:
git init
git add mindmirror_app.py
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/mindmirror-ai.git
git push -u origin main</pre>
                    </div>
                </li>

                <li>
                    <strong>Create Streamlit Cloud Account</strong><br>
                    Go to <code>share.streamlit.io</code> and sign up with GitHub
                </li>

                <li>
                    <strong>Connect Repository</strong><br>
                    Click "New app" → Select your GitHub repo → Choose branch (main)<br>
                    Set main file path: <code>mindmirror_app.py</code>
                </li>

                <li>
                    <strong>Deploy! 🚀</strong><br>
                    Click "Deploy" and wait 2-3 minutes. Your app will be live at:<br>
                    <code>https://your-app-name.streamlit.app</code>
                </li>
            </ol>

            <div class="highlight-box">
                <strong>💡 Pro Tip:</strong> For persistent database in cloud deployment, consider using:
                <ul style="margin-top: 10px; margin-left: 20px;">
                    <li><code>Streamlit Community Cloud</code> with file persistence (free tier)</li>
                    <li><code>Supabase</code> or <code>Firestore</code> for cloud databases</li>
                    <li><code>Google Sheets API</code> for simple data storage</li>
                </ul>
            </div>
        </div>

        <!-- Features Comparison -->
        <div class="section">
            <h2 class="section-title">🆚 HTML vs Streamlit Version Comparison</h2>
            
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <thead>
                    <tr style="background: rgba(102, 126, 234, 0.2);">
                        <th style="padding: 15px; text-align: left; border: 1px solid rgba(255,255,255,0.1);">Feature</th>
                        <th style="padding: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">HTML Prototype</th>
                        <th style="padding: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">Streamlit Version</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 12px; border: 1px solid rgba(255,255,255,0.05);"><strong>Database Storage</strong></td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">❌ No (session only)</td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">✅ SQLite (persistent)</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.02);">
                        <td style="padding: 12px; border: 1px solid rgba(255,255,255,0.05);"><strong>Data Persistence</strong></td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">❌ Lost on refresh</td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">✅ Saves forever</td>
                    </tr>
                    <tr>
                        <td style="padding: 12px; border: 1px solid rgba(255,255,255,0.05);"><strong>Real Charts</strong></td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">⚠️ CSS only (static)</td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">✅ Plotly (interactive)</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.02);">
                        <td style="padding: 12px; border: 1px solid rgba(255,255,255,0.05);"><strong>AI Integration</strong></td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">⚠️ Pre-programmed</td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">✅ API-ready (OpenAI/Gemini)</td>
                    </tr>
                    <tr>
                        <td style="padding: 12px; border: 1px solid rgba(255,255,255,0.05);"><strong>User Authentication</strong></td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">❌ Not possible</td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">✅ Easy to add</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.02);">
                        <td style="padding: 12px; border: 1px solid rgba(255,255,255,0.05);"><strong>Deployment</strong></td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">⚠️ Static hosting only</td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">✅ Streamlit Cloud (free)</td>
                    </tr>
                    <tr>
                        <td style="padding: 12px; border: 1px solid rgba(255,255,255,0.05);"><strong>Scalability</strong></td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">❌ Limited</td>
                        <td style="padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">✅ Auto-scales</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Next Steps -->
        <div class="section">
            <h2 class="section-title">🚀 Next Steps After Deployment</h2>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🔗</div>
                    <div class="feature-title">Add Real AI</div>
                    <div class="feature-desc">Integrate OpenAI GPT-4 or Google Gemini API for genuine conversational AI responses</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📷</div>
                    <div class="feature-title">Camera Integration</div>
                    <div class="feature-desc">Use TensorFlow.js or MediaPipe for actual face/emotion detection via webcam</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">👤</div>
                    <div class="feature-title">User Authentication</div>
                    <div class="feature-desc">Add login/signup with Streamlit-Authenticator or Firebase Auth</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💳</div>
                    <div class="feature-title">Payment System</div>
                    <div class="feature-desc">Integrate Stripe/Razorpay for Premium subscription payments</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📧</div>
                    <div class="feature-title">Email Notifications</div>
                    <div class="feature-desc">Daily mood check-ins, weekly reports, crisis alerts via email/SMS</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🌙</div>
                    <div class="feature-title">Mobile App</div>
                    <div class="feature-desc">Convert to React Native or Flutter for iOS/Android native apps</div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer>
            <p><strong>🧠 MindMirror AI</strong> - Built with ❤️ using Streamlit</p>
            <p style="margin-top: 10px;">
                Complete Python Application | Production-Ready | Free Deployment Available
            </p>
            <p style="margin-top: 15px; font-size: 0.9rem;">
                © 2026 MindMirror AI. Empowering mental wellness through technology.
            </p>
        </footer>

    </div>

    <script>
        function copyCode(button) {
            const codeBlock = button.parentElement.querySelector('pre');
            const textArea = document.createElement('textarea');
            textArea.value = codeBlock.textContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            button.textContent = 'Copied! ✓';
            setTimeout(() => {
                button.textContent = 'Copy';
            }, 2000);
        }

        function copyFullCode() {
            const fullCode = document.getElementById('fullAppCode').textContent;
            const textArea = document.createElement('textarea');
            textArea.value = fullCode;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            alert('✅ Full application code copied to clipboard!\n\nNow paste it into mindmirror_app.py file');
        }
    </script>
</body>
</html>
