import streamlit as st
import plotly.graph_objects as go
import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from pydub import AudioSegment
import io
import tempfile
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Data Notes - Data Sonification",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .recording-status {
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .recording-active {
        background-color: #ffebee;
        border: 2px solid #f44336;
        color: #c62828;
    }
    .recording-inactive {
        background-color: #e8f5e8;
        border: 2px solid #4caf50;
        color: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample line graph data"""
    x = np.linspace(0, 10, 100)
    # Create an interesting waveform with multiple frequencies
    y = (np.sin(x) * 0.5 + 
         np.sin(2*x) * 0.3 + 
         np.sin(0.5*x) * 0.2 + 
         np.random.normal(0, 0.1, len(x)))
    return x, y

def create_line_graph(x, y):
    """Create an interactive line graph using Plotly"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Data Waveform',
        line=dict(color='#1f77b4', width=3),
        fill='tonexty',
        fillcolor='rgba(31, 119, 180, 0.1)'
    ))
    
    fig.update_layout(
        title={
            'text': 'Data Waveform - Observe and Describe',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='Time',
        yaxis_title='Amplitude',
        height=400,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

def apply_waveform_modulation(audio_data, sample_rate, waveform_data):
    """Apply waveform modulation to audio based on graph data"""
    # Normalize waveform data to audio length
    audio_length = len(audio_data)
    waveform_resampled = signal.resample(waveform_data, audio_length)
    
    # Normalize waveform to reasonable modulation range
    waveform_normalized = waveform_resampled / np.max(np.abs(waveform_resampled)) * 0.3
    
    # Apply modulation
    modulated_audio = audio_data * (1 + waveform_normalized)
    
    # Ensure we don't clip
    if np.max(np.abs(modulated_audio)) > 1.0:
        modulated_audio = modulated_audio / np.max(np.abs(modulated_audio)) * 0.95
    
    return modulated_audio

def save_audio(audio_data, sample_rate, filename):
    """Save audio data to a temporary file"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    sf.write(temp_file.name, audio_data, sample_rate)
    return temp_file.name

def main():
    # Header
    st.markdown('<h1 class="main-header">Data Notes</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Data Sonification Through Voice Modulation</p>', unsafe_allow_html=True)
    
    # Information box
    st.markdown("""
    <div class="info-box">
        <strong>How it works:</strong><br>
        1. Observe the line graph below<br>
        2. Record your description of what you see<br>
        3. Listen to your voice modulated by the waveform data<br>
        4. Experience data sonification through voice transformation
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample data
    x, y = generate_sample_data()
    
    # Create and display the graph
    fig = create_line_graph(x, y)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recording section
    st.markdown("## Voice Recording")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Recording controls
        if 'recording' not in st.session_state:
            st.session_state.recording = False
        if 'audio_data' not in st.session_state:
            st.session_state.audio_data = None
        if 'sample_rate' not in st.session_state:
            st.session_state.sample_rate = None
        
        # Recording status display
        if st.session_state.recording:
            st.markdown('<div class="recording-status recording-active">🎙️ Recording... Speak now!</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="recording-status recording-inactive">⏸️ Ready to record</div>', 
                       unsafe_allow_html=True)
        
        # Recording buttons
        if not st.session_state.recording:
            if st.button("🎙️ Start Recording", type="primary", use_container_width=True):
                st.session_state.recording = True
                st.rerun()
        else:
            if st.button("⏹️ Stop Recording", type="secondary", use_container_width=True):
                st.session_state.recording = False
                # Simulate recording (in a real app, this would use actual audio recording)
                st.session_state.audio_data = np.random.rand(44100 * 3)  # 3 seconds of random audio
                st.session_state.sample_rate = 44100
                st.rerun()
    
    # Audio playback section
    if st.session_state.audio_data is not None:
        st.markdown("## Audio Playback")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Original Recording")
            st.audio(st.session_state.audio_data, sample_rate=st.session_state.sample_rate)
        
        with col2:
            st.markdown("### Waveform-Modulated Audio")
            # Apply waveform modulation
            modulated_audio = apply_waveform_modulation(
                st.session_state.audio_data, 
                st.session_state.sample_rate, 
                y
            )
            st.audio(modulated_audio, sample_rate=st.session_state.sample_rate)
        
        # Download options
        st.markdown("### Download Audio")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download Original", use_container_width=True):
                # Save and provide download for original
                original_file = save_audio(st.session_state.audio_data, st.session_state.sample_rate, "original")
                with open(original_file, 'rb') as f:
                    st.download_button(
                        label="Download Original Audio",
                        data=f.read(),
                        file_name=f"original_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                        mime="audio/wav"
                    )
                os.unlink(original_file)
        
        with col2:
            if st.button("📥 Download Modulated", use_container_width=True):
                # Save and provide download for modulated
                modulated_file = save_audio(modulated_audio, st.session_state.sample_rate, "modulated")
                with open(modulated_file, 'rb') as f:
                    st.download_button(
                        label="Download Modulated Audio",
                        data=f.read(),
                        file_name=f"modulated_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                        mime="audio/wav"
                    )
                os.unlink(modulated_file)
    
    # Instructions and tips
    with st.expander("💡 Tips for Best Results"):
        st.markdown("""
        - **Clear speech**: Speak clearly and at a moderate pace
        - **Detailed descriptions**: Describe patterns, trends, and interesting features you observe
        - **Multiple recordings**: Try recording different observations to hear various modulation effects
        - **Headphones recommended**: Use headphones for the best audio experience
        - **Experiment**: Try different graphs and see how the modulation changes
        """)
    
    # About section
    with st.expander("ℹ️ About Data Notes"):
        st.markdown("""
        **Data Notes** is an experimental data sonification tool that transforms your voice using the waveform of data.
        
        **How the modulation works:**
        - Your voice recording is analyzed and processed
        - The line graph data is used as a modulation envelope
        - The amplitude and frequency characteristics of the data affect your voice
        - This creates a unique audio experience that connects data visualization with sound
        
        **Applications:**
        - Data exploration and analysis
        - Educational demonstrations of data sonification
        - Creative audio-visual experiences
        - Accessibility tools for data interpretation
        """)

if __name__ == "__main__":
    main()
