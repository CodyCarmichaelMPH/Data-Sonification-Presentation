#!/usr/bin/env python3
"""
Data Notes - Version Comparison Demo

This script demonstrates the differences between the simple and real-time versions
of the Data Notes application.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Data Notes - Version Comparison",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .version-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
        color: #2c3e50;
    }
    .version-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .feature-list {
        list-style-type: none;
        padding-left: 0;
        color: #2c3e50;
    }
    .feature-list li {
        padding: 0.25rem 0;
        border-bottom: 1px solid #eee;
        font-weight: 500;
    }
    .feature-list li:before {
        content: "✅ ";
        color: #28a745;
        font-weight: bold;
    }
    .demo-button {
        margin-top: 1rem;
    }
    /* Improve general text contrast */
    .stMarkdown {
        color: #2c3e50;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1a1a1a;
        font-weight: 600;
    }
    .stMarkdown p {
        color: #2c3e50;
        line-height: 1.6;
    }
    /* Improve table text */
    .stTable {
        color: #2c3e50;
    }
    .stTable th {
        color: #1a1a1a;
        font-weight: 600;
    }
    .stTable td {
        color: #2c3e50;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🎵 Data Notes - Version Comparison")
    st.markdown("### Choose the version that best suits your needs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="version-card">
            <div class="version-title">Simple Version (app_simple.py)</div>
            <ul class="feature-list">
                <li>Simulated audio recording</li>
                <li>No microphone required</li>
                <li>Perfect for testing and demos</li>
                <li>Works in any environment</li>
                <li>Minimal dependencies</li>
                <li>Fast setup and execution</li>
                <li>Good for educational purposes</li>
            </ul>
            <div class="demo-button">
                <a href="http://localhost:8501" target="_blank">
                    <button style="background-color: #28a745; color: white; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; cursor: pointer;">
                        🚀 Launch Simple Version
                    </button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="version-card">
            <div class="version-title">Real-time Version (app_realtime.py)</div>
            <ul class="feature-list">
                <li>Live microphone recording</li>
                <li>Real-time audio processing</li>
                <li>WebRTC-based audio capture</li>
                <li>High-quality 44.1kHz audio</li>
                <li>Instant modulation effects</li>
                <li>Full data sonification experience</li>
                <li>Requires microphone access</li>
            </ul>
            <div class="demo-button">
                <a href="http://localhost:8502" target="_blank">
                    <button style="background-color: #007bff; color: white; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; cursor: pointer;">
                        🎙️ Launch Real-time Version
                    </button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technical comparison
    st.markdown("## Technical Comparison")
    
    comparison_data = {
        "Feature": [
            "Audio Recording",
            "Dependencies",
            "Setup Time",
            "Browser Requirements",
            "Audio Quality",
            "Real-time Processing",
            "Use Case"
        ],
        "Simple Version": [
            "Simulated",
            "Minimal (3 packages)",
            "Fast (< 1 min)",
            "Any browser",
            "Demo quality",
            "No",
            "Testing & Education"
        ],
        "Real-time Version": [
            "Live microphone",
            "Full stack (8+ packages)",
            "Moderate (2-3 min)",
            "Modern browser + HTTPS",
            "High quality (44.1kHz)",
            "Yes",
            "Production & Research"
        ]
    }
    
    st.table(comparison_data)
    
    # Usage instructions
    st.markdown("## How to Use")
    
    st.markdown("""
    ### For Simple Version:
    1. Run `streamlit run app_simple.py`
    2. Open browser to `http://localhost:8501`
    3. Click "Start Recording" (simulated)
    4. Click "Stop Recording" to generate demo audio
    5. Listen to modulated audio
    
    ### For Real-time Version:
    1. Run `streamlit run app_realtime.py`
    2. Open browser to `http://localhost:8501`
    3. Allow microphone access when prompted
    4. Click "Start Recording" and speak
    5. Click "Stop Recording" when done
    6. Listen to your voice modulated by the data
    """)
    
    # Tips section
    st.markdown("## Tips for Best Experience")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Simple Version Tips:**
        - Great for understanding the concept
        - Use headphones to hear the modulation clearly
        - Try different descriptions to see various effects
        - Perfect for classroom demonstrations
        """)
    
    with col2:
        st.markdown("""
        **Real-time Version Tips:**
        - Use a quiet environment
        - Speak clearly and at moderate pace
        - Describe patterns you observe in detail
        - Try multiple recordings for different effects
        - Use Chrome/Chromium for best compatibility
        """)

if __name__ == "__main__":
    main()
