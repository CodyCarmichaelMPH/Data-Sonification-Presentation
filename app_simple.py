import streamlit as st
import plotly.graph_objects as go
import numpy as np
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
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        color: #2c3e50;
        font-weight: 500;
    }
    .info-box strong {
        color: #1a1a1a;
        font-weight: 700;
    }
    .recording-status {
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .recording-active {
        background-color: #ffebee;
        border: 2px solid #f44336;
        color: #b71c1c;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .recording-inactive {
        background-color: #e8f5e8;
        border: 2px solid #4caf50;
        color: #1b5e20;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .audio-player {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        color: #2c3e50;
    }
    .audio-player h3 {
        color: #1a1a1a;
        font-weight: 600;
        margin-bottom: 0.5rem;
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
    /* Improve button text contrast */
    .stButton > button {
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    /* Improve caption text */
    .stCaption {
        color: #495057;
        font-weight: 500;
    }
    /* Improve expander text */
    .streamlit-expanderHeader {
        color: #1a1a1a;
        font-weight: 600;
    }
    .streamlit-expanderContent {
        color: #2c3e50;
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

def create_audio_visualization(audio_data, title):
    """Create a simple waveform visualization for audio"""
    if audio_data is None or len(audio_data) == 0:
        return None
    
    # Downsample for visualization
    downsample_factor = max(1, len(audio_data) // 1000)
    audio_vis = audio_data[::downsample_factor]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=audio_vis,
        mode='lines',
        line=dict(color='#2ecc71', width=1),
        name='Audio Waveform'
    ))
    
    fig.update_layout(
        title=title,
        height=150,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    fig.update_xaxes(showgrid=False, showticklabels=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

def apply_waveform_modulation(audio_data, waveform_data):
    """Apply waveform modulation to audio based on graph data"""
    if audio_data is None or len(audio_data) == 0:
        return None
    
    # Simple modulation: multiply audio by waveform envelope
    # Normalize waveform to audio length
    audio_length = len(audio_data)
    waveform_resampled = np.interp(
        np.linspace(0, 1, audio_length),
        np.linspace(0, 1, len(waveform_data)),
        waveform_data
    )
    
    # Normalize waveform to reasonable modulation range
    waveform_normalized = waveform_resampled / np.max(np.abs(waveform_resampled)) * 0.3
    
    # Apply modulation
    modulated_audio = audio_data * (1 + waveform_normalized)
    
    # Ensure we don't clip
    if np.max(np.abs(modulated_audio)) > 1.0:
        modulated_audio = modulated_audio / np.max(np.abs(modulated_audio)) * 0.95
    
    return modulated_audio

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
            st.session_state.sample_rate = 44100
        
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
                # Create a simulated audio signal with some variation
                duration = 3  # seconds
                sample_rate = 44100
                t = np.linspace(0, duration, int(sample_rate * duration))
                
                # Create a simulated voice signal
                voice_freq = 200  # Hz
                voice_signal = np.sin(2 * np.pi * voice_freq * t) * 0.5
                
                # Add some variation to make it more realistic
                voice_signal += np.sin(2 * np.pi * 400 * t) * 0.2  # harmonics
                voice_signal += np.random.normal(0, 0.1, len(t))  # noise
                
                st.session_state.audio_data = voice_signal
                st.session_state.sample_rate = sample_rate
                st.rerun()
    
    # Audio playback section
    if st.session_state.audio_data is not None:
        st.markdown("## Audio Playback")
        
        audio_data = st.session_state.audio_data
        sample_rate = st.session_state.sample_rate
        
        # Calculate duration
        duration = len(audio_data) / sample_rate
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Original Recording")
            st.markdown(f"<div class='audio-player'>", unsafe_allow_html=True)
            st.audio(audio_data, sample_rate=sample_rate)
            st.caption(f"Duration: {duration:.2f} seconds")
            
            # Audio visualization
            vis_fig = create_audio_visualization(audio_data, "Original Audio Waveform")
            if vis_fig:
                st.plotly_chart(vis_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Waveform-Modulated Audio")
            # Apply waveform modulation
            modulated_audio = apply_waveform_modulation(audio_data, y)
            
            if modulated_audio is not None:
                st.markdown(f"<div class='audio-player'>", unsafe_allow_html=True)
                st.audio(modulated_audio, sample_rate=sample_rate)
                st.caption(f"Duration: {duration:.2f} seconds")
                
                # Modulated audio visualization
                mod_vis_fig = create_audio_visualization(modulated_audio, "Modulated Audio Waveform")
                if mod_vis_fig:
                    st.plotly_chart(mod_vis_fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Download options
                st.markdown("### Download Audio")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📥 Download Original", use_container_width=True):
                        # Create a simple text file with audio data for demonstration
                        original_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
                        np.savetxt(original_file.name, audio_data)
                        with open(original_file.name, 'rb') as f:
                            st.download_button(
                                label="Download Original Audio Data",
                                data=f.read(),
                                file_name=f"original_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain"
                            )
                        os.unlink(original_file.name)
                
                with col2:
                    if st.button("📥 Download Modulated", use_container_width=True):
                        # Create a simple text file with modulated audio data for demonstration
                        modulated_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
                        np.savetxt(modulated_file.name, modulated_audio)
                        with open(modulated_file.name, 'rb') as f:
                            st.download_button(
                                label="Download Modulated Audio Data",
                                data=f.read(),
                                file_name=f"modulated_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain"
                            )
                        os.unlink(modulated_file.name)
            else:
                st.error("Failed to create modulated audio.")
    
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
        
        **Note:** This is a simplified demonstration version. The full version includes real microphone recording capabilities.
        """)
    
    # Technical information
    with st.expander("🔧 Technical Information"):
        st.markdown("""
        **Audio Processing Pipeline:**
        1. **Recording**: Simulated audio generation (demo mode)
        2. **Processing**: Waveform analysis and modulation
        3. **Modulation**: Graph data applied as amplitude envelope
        4. **Output**: Audio visualization and data export
        
        **Dependencies:**
        - Streamlit for web interface
        - NumPy for numerical processing
        - Plotly for data visualization
        
        **Demo Features:**
        - Simulated voice recording for testing
        - Real-time waveform modulation
        - Audio visualization
        - Data export capabilities
        """)

if __name__ == "__main__":
    main()
