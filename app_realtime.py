import streamlit as st
import plotly.graph_objects as go
import numpy as np
import tempfile
import os
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import threading
import queue
import time
import soundfile as sf
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Data Notes - Voice Waveform Transformation",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for black text on white backgrounds
st.markdown("""
<style>
    /* Force ALL backgrounds to white and ALL text to black */
    .main .block-container {
        background-color: #ffffff !important;
        padding-top: 2rem;
    }
    
    /* Headers - Black text on white background */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #000000 !important;
        margin-bottom: 1rem;
        background-color: #ffffff !important;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #000000;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        background-color: #ffffff !important;
    }
    
    /* Graph container - White background */
    .graph-container {
        background-color: #ffffff !important;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #000000;
        margin-bottom: 2rem;
    }
    
    /* Recording section - White background */
    .recording-section {
        background-color: #ffffff !important;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #000000;
        margin-bottom: 2rem;
    }
    
    /* Recording status - Black text on white background */
    .recording-status {
        text-align: center;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        border: 2px solid #000000;
    }
    
    .recording-active {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 3px solid #ff0000;
        animation: pulse 1.5s infinite;
    }
    
    .recording-inactive {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000;
    }
    
    /* Pulse animation */
    @keyframes pulse {
        0% { border-color: #ff0000; }
        50% { border-color: #ff6666; }
        100% { border-color: #ff0000; }
    }
    
    /* Audio player container - White background */
    .audio-container {
        background-color: #ffffff !important;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #000000;
        margin-bottom: 1rem;
    }
    
    .audio-container h3 {
        color: #000000 !important;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #000000;
        padding-bottom: 0.5rem;
        background-color: #ffffff !important;
    }
    
    /* ALL Buttons - Black text on white background */
    .stButton > button {
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #000000 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        background-color: #f8f9fa !important;
        color: #000000 !important;
    }
    
    /* ALL Text elements - Black on white */
    .stMarkdown, .stMarkdown *, div[data-testid="stMarkdown"], 
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p,
    .stCaption, .streamlit-expanderHeader, .streamlit-expanderContent,
    .stAlert, .stSuccess, .stError, .stWarning, .stInfo {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide WebRTC streamer default UI completely */
    [data-testid="stWebRtcStreamer"] {
        display: none !important;
    }
    
    /* Force ALL elements to have white background and black text */
    * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Override any Streamlit default colors */
    .stApp {
        background-color: #ffffff !important;
    }
    
    .stApp > header {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    .stApp > main {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Audio player styling */
    audio {
        background-color: #ffffff !important;
        border: 2px solid #000000 !important;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

class AudioRecorder:
    def __init__(self):
        self.audio_frames = []
        self.is_recording = False
        self.sample_rate = 44100
        self.recording_start_time = None
        
    def audio_frame_callback(self, frame):
        """Process incoming audio frames"""
        if self.is_recording:
            try:
                audio_array = frame.to_ndarray()
                if audio_array is not None and len(audio_array) > 0:
                    self.audio_frames.append(audio_array)
            except Exception as e:
                st.error(f"Audio processing error: {str(e)}")
        return frame
    
    def start_recording(self):
        """Start recording audio"""
        self.audio_frames = []
        self.is_recording = True
        self.recording_start_time = time.time()
        
    def stop_recording(self):
        """Stop recording and return processed audio"""
        self.is_recording = False
        
        if not self.audio_frames:
            return None
            
        try:
            # Concatenate all audio frames
            audio_data = np.concatenate(self.audio_frames, axis=0)
            
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Ensure minimum recording length
            if len(audio_data) < 4410:  # Less than 0.1 seconds
                return None
                
            # Normalize audio
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
                
            return audio_data
            
        except Exception as e:
            st.error(f"Audio processing error: {str(e)}")
            return None
    
    def get_recording_duration(self):
        """Get current recording duration"""
        if self.recording_start_time and self.is_recording:
            return time.time() - self.recording_start_time
        return 0

def generate_waveform_data():
    """Generate an interesting waveform for visualization"""
    x = np.linspace(0, 10, 200)
    
    # Create a complex waveform with multiple frequencies
    y = (np.sin(x) * 0.4 + 
         np.sin(2.5 * x) * 0.3 + 
         np.sin(0.7 * x) * 0.2 + 
         np.cos(1.8 * x) * 0.15 +
         np.random.normal(0, 0.05, len(x)))
    
    return x, y

def create_waveform_plot(x, y):
    """Create the main waveform visualization"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Waveform',
        line=dict(color='#000000', width=3),
        fill='tonexty',
        fillcolor='rgba(0, 0, 0, 0.1)'
    ))
    
    fig.update_layout(
        title={
            'text': '📊 Observe this waveform and describe what you see',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#000000'}
        },
        xaxis_title='Time',
        yaxis_title='Amplitude',
        height=400,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#cccccc',
            zeroline=False,
            color='#000000'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#cccccc',
            zeroline=False,
            color='#000000'
        )
    )
    
    return fig

def create_audio_visualization(audio_data, title):
    """Create audio waveform visualization"""
    if audio_data is None or len(audio_data) == 0:
        return None
    
    # Downsample for visualization
    downsample_factor = max(1, len(audio_data) // 1000)
    audio_vis = audio_data[::downsample_factor]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=audio_vis,
        mode='lines',
        line=dict(color='#000000', width=1.5),
        name='Audio'
    ))
    
    fig.update_layout(
        title=title,
        height=120,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#cccccc',
            zeroline=False,
            color='#000000'
        )
    )
    
    return fig

def apply_waveform_transformation(audio_data, waveform_data):
    """Apply waveform transformation to audio"""
    if audio_data is None or len(audio_data) == 0:
        return None
    
    try:
        audio_length = len(audio_data)
        
        # Resample waveform to match audio length
        waveform_resampled = np.interp(
            np.linspace(0, 1, audio_length),
            np.linspace(0, 1, len(waveform_data)),
            waveform_data
        )
        
        # Normalize waveform for modulation
        waveform_normalized = waveform_resampled / np.max(np.abs(waveform_resampled)) * 0.4
        
        # Apply amplitude modulation
        transformed_audio = audio_data * (1 + waveform_normalized)
        
        # Prevent clipping
        if np.max(np.abs(transformed_audio)) > 1.0:
            transformed_audio = transformed_audio / np.max(np.abs(transformed_audio)) * 0.95
        
        return transformed_audio
        
    except Exception as e:
        st.error(f"Transformation error: {str(e)}")
        return None

def save_audio_to_bytes(audio_data, sample_rate, format='wav'):
    """Save audio data to bytes for download"""
    try:
        buffer = BytesIO()
        sf.write(buffer, audio_data, sample_rate, format=format)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Audio save error: {str(e)}")
        return None

def create_audio_recorder():
    """Create WebRTC audio recorder"""
    rtc_configuration = RTCConfiguration({
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {"urls": ["stun:stun1.l.google.com:19302"]}
        ]
    })
    
    if 'audio_recorder' not in st.session_state:
        st.session_state.audio_recorder = AudioRecorder()
    
    recorder = st.session_state.audio_recorder
    
    # Create WebRTC streamer without showing the default button
    webrtc_ctx = webrtc_streamer(
        key="audio-recorder",
        mode=WebRtcMode.SENDONLY,
        audio_frame_callback=recorder.audio_frame_callback,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={
            "video": False,
            "audio": {
                "sampleRate": 44100,
                "channelCount": 1,
                "echoCancellation": True,
                "noiseSuppression": True,
                "autoGainControl": True
            }
        },
        async_processing=True
    )
    
    return webrtc_ctx, recorder

def main():
    # Header
    st.markdown('<h1 class="main-header">Data Notes</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your voice with data waveforms</p>', unsafe_allow_html=True)
    
    # Data Sonification Explanation
    st.markdown("## What is Data Sonification?")
    st.markdown("""
    **Data sonification** is the process of converting data into sound. Just as we use charts and graphs to visualize data patterns, 
    sonification allows us to "hear" data through audio representations. This technique helps us:
    
    - **Discover patterns** that might be invisible in visual representations
    - **Process information** through our auditory system, which can detect subtle changes and rhythms
    - **Access data** in new ways, especially useful for people with visual impairments
    - **Enhance understanding** by combining visual and auditory information
    
    In this application, we're exploring how data patterns can transform human speech, creating a bridge between 
    data analysis and creative expression.
    """)
    
    # Example Section Header
    st.markdown("## Example: Waveform Transformation")
    st.markdown("Below is a sample waveform. Try recording your voice while describing what you observe, then listen to how the data transforms your speech.")
    
    # Step 1: Display the waveform
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    x, y = generate_waveform_data()
    fig = create_waveform_plot(x, y)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Voice recording section
    st.markdown('<div class="recording-section">', unsafe_allow_html=True)
    st.markdown("## 🎙️ Record Your Voice")
    
    # Create audio recorder
    webrtc_ctx, recorder = create_audio_recorder()
    
    # Recording interface - Single button design
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Recording status display
        if recorder.is_recording:
            duration = recorder.get_recording_duration()
            st.markdown(
                f'<div class="recording-status recording-active">🎙️ Recording... {duration:.1f}s</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="recording-status recording-inactive">⏸️ Ready to record</div>',
                unsafe_allow_html=True
            )
        
        # Single recording control button
        try:
            if hasattr(webrtc_ctx, 'state') and webrtc_ctx.state is not None:
                if not recorder.is_recording:
                    if st.button("🎙️ Start Recording", use_container_width=True):
                        recorder.start_recording()
                        st.rerun()
                else:
                    if st.button("⏹️ Stop Recording", use_container_width=True):
                        audio_data = recorder.stop_recording()
                        if audio_data is not None:
                            st.session_state.original_audio = audio_data
                            st.session_state.sample_rate = recorder.sample_rate
                            st.success("✅ Recording completed!")
                        else:
                            st.error("❌ Recording failed. Please try again.")
                        st.rerun()
            else:
                st.info("🔄 Initializing microphone... Please wait.")
        except Exception as e:
            st.error(f"❌ Recording error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3: Audio playback section
    if 'original_audio' in st.session_state and st.session_state.original_audio is not None:
        st.markdown("## 🔊 Audio Playback")
        
        original_audio = st.session_state.original_audio
        sample_rate = st.session_state.sample_rate
        duration = len(original_audio) / sample_rate
        
        # Apply transformation
        transformed_audio = apply_waveform_transformation(original_audio, y)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="audio-container">', unsafe_allow_html=True)
            st.markdown("### 🎵 Original Recording")
            st.audio(original_audio, sample_rate=sample_rate)
            st.caption(f"Duration: {duration:.2f} seconds")
            
            # Original audio visualization
            orig_vis = create_audio_visualization(original_audio, "Original Waveform")
            if orig_vis:
                st.plotly_chart(orig_vis, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="audio-container">', unsafe_allow_html=True)
            st.markdown("### 🎛️ Transformed Audio")
            
            if transformed_audio is not None:
                st.audio(transformed_audio, sample_rate=sample_rate)
                st.caption(f"Duration: {duration:.2f} seconds")
                
                # Transformed audio visualization
                trans_vis = create_audio_visualization(transformed_audio, "Transformed Waveform")
                if trans_vis:
                    st.plotly_chart(trans_vis, use_container_width=True)
            else:
                st.error("❌ Transformation failed")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Download section
        if transformed_audio is not None:
            st.markdown("## 📥 Download Audio")
            col1, col2 = st.columns(2)
            
            with col1:
                original_bytes = save_audio_to_bytes(original_audio, sample_rate)
                if original_bytes:
                    st.download_button(
                        label="📥 Download Original",
                        data=original_bytes,
                        file_name=f"original_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                        mime="audio/wav",
                        use_container_width=True
                    )
            
            with col2:
                transformed_bytes = save_audio_to_bytes(transformed_audio, sample_rate)
                if transformed_bytes:
                    st.download_button(
                        label="📥 Download Transformed",
                        data=transformed_bytes,
                        file_name=f"transformed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                        mime="audio/wav",
                        use_container_width=True
                    )
    
    # Voice Interpretation Section
    st.markdown("## Did your voice sound weird or hard to understand?")
    st.markdown("""
    This is actually a common experience with data sonification! Here's why:
    
    **The Challenge of Interpretation:**
    - **Data patterns** can create complex audio effects that distort natural speech
    - **Amplitude modulation** from the waveform can make words sound choppy or robotic
    - **Frequency changes** might alter the pitch and clarity of your voice
    - **Rhythm interference** between your speech patterns and the data patterns can create confusion
    
    **Why This Happens:**
    When we apply data waveforms to human speech, we're essentially "modulating" your voice with mathematical patterns. 
    While these patterns might be easy to interpret visually (especially if you know the underlying data), 
    they can create audio that's challenging to understand because:
    
    - Human speech has its own natural rhythms and patterns
    - Data patterns may not align with linguistic structures
    - Our brains are optimized for processing natural speech, not modulated versions
    
    **The Learning Opportunity:**
    This difficulty in interpretation actually highlights an important aspect of data sonification - 
    it requires practice and context to become effective. Just as we learn to read charts and graphs, 
    we can develop skills to "hear" data patterns more clearly over time.
    """)
    
    # Instructions
    with st.expander("💡 How to use"):
        st.markdown("""
        **Simple 4-step process:**
        
        1. **📊 Observe** the waveform graph above
        2. **🎙️ Record** your voice describing what you see
        3. **🎛️ Transform** your voice with the waveform
        4. **🔊 Listen** to both original and transformed audio
        
        **Tips for best results:**
        - Speak clearly and describe patterns you observe
        - Record for at least 2-3 seconds
        - Use headphones for better audio experience
        - Try different descriptions to hear various effects
        """)
    
    # About section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Data Notes** transforms your voice using data waveforms, creating a unique audio-visual experience.
        
        The transformation applies the amplitude characteristics of the waveform to your voice recording,
        creating a modulated version that reflects the data patterns you observed.
        
        Built with Streamlit, WebRTC, and real-time audio processing.
        """)

if __name__ == "__main__":
    main()
