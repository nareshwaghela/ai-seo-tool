# ============================================
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

    @import url('https://artifacts-cdn.chatglm.site/https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
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

    🧠 MindMirror AI
    Your AI-Powered Emotional Wellness Companion

""", unsafe_allow_html=True)

# Create columns for main dashboard
col1, col2 = st.columns(2)

# ============================================
# COLUMN 1: EMOTION DETECTION + MOOD TRACKER
# ============================================

with col1:
    # Emotion Detection Card
    st.markdown('', unsafe_allow_html=True)
    st.subheader("📸 Real-Time Emotion Detection")
    
    if not st.session_state.scan_completed:
        st.markdown("""
        
            📷
            Tap below to analyze your facial expression
        
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
        
            {emotion['emoji']}
            
                {emotion['name']}
            
            
                Confidence Level: {emotion['confidence']}%
            
            
                
            
        
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Scan Again", key="reset_scan_btn", use_container_width=True):
            st.session_state.scan_completed = False
            st.session_state.current_emotion = None
            st.rerun()
    
    st.markdown('', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mood Tracker Card
    st.markdown('', unsafe_allow_html=True)
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
    
    st.markdown('', unsafe_allow_html=True)

# ============================================
# COLUMN 2: AI CHAT + ANALYTICS
# ============================================

with col2:
    # AI Chat Interface
    st.markdown('', unsafe_allow_html=True)
    st.subheader("🤖 AI Wellness Companion")
    
    # Display chat messages
    chat_container = st.container(height=400)
    
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"😊 {msg['content']}", unsafe_allow_html=True)
            else:
                st.markdown(f"🤖 {msg['content']}", unsafe_allow_html=True)
    
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
    
    st.markdown('', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analytics Dashboard
    st.markdown('', unsafe_allow_html=True)
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
    
    st.markdown('', unsafe_allow_html=True)

# ============================================
# BOTTOM SECTION: RECOMMENDATIONS
# ============================================

st.markdown("---")

st.subheader("🎯 Personalized Recommendations For You")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    with st.container():
        st.markdown("""
        
            🧘
            Morning Mindfulness Meditation
            
                Start your day with clarity. This 10-minute guided session helps reduce anxiety.
            
            ⏱️ 10 mins • Beginner Friendly
        
        """, unsafe_allow_html=True)

with rec_col2:
    with st.container():
        st.markdown("""
        
            🌬️
            4-7-8 Breathing Exercise
            
                Instant stress relief technique. Calms your nervous system in just 2 minutes.
            
            ⏱️ 2 mins • Quick Relief
        
        """, unsafe_allow_html=True)

rec_col3, rec_col4 = st.columns(2)

with rec_col3:
    with st.container():
        st.markdown("""
        
            📝
            Gratitude Journaling Prompt
            
                Research shows gratitude practice increases happiness by 25%.
            
            ⏱️ 5 mins • Mood Booster
        
        """, unsafe_allow_html=True)

with rec_col4:
    with st.container():
        st.markdown("""
        
            🎵
            Calming Ambient Playlist
            
                Curated nature sounds and soft melodies to help you relax deeply.
            
            ⏱️ 45 mins • Sleep Aid
        
        """, unsafe_allow_html=True)

# ============================================
# SIDEBAR CONFIGURATION
# ============================================

with st.sidebar:
    st.markdown("### 👤 User Profile")
    st.markdown("""
    
        😊
        Welcome Back!
        Premium Member ✨
    
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

    © 2026 MindMirror AI | Made with 💜 for better mental health everywhere
    
        Disclaimer: Not a substitute for professional medical advice. If you're in crisis, please call emergency services immediately.
    

""", unsafe_allow_html=True)
