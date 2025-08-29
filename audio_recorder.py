import streamlit as st
import numpy as np
import soundfile as sf
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import threading
import queue
import time

class AudioRecorder:
    def __init__(self):
        self.audio_frames = []
        self.recording = False
        self.sample_rate = 44100
        
    def audio_frame_callback(self, frame):
        """Callback for processing audio frames"""
        if self.recording:
            # Convert frame to numpy array
            audio_array = frame.to_ndarray()
            self.audio_frames.append(audio_array)
        return frame
    
    def start_recording(self):
        """Start recording audio"""
        self.audio_frames = []
        self.recording = True
        
    def stop_recording(self):
        """Stop recording and return audio data"""
        self.recording = False
        if self.audio_frames:
            # Concatenate all audio frames
            audio_data = np.concatenate(self.audio_frames, axis=0)
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            return audio_data
        return None

def create_audio_recorder():
    """Create and return an audio recorder component"""
    
    # RTC Configuration for WebRTC
    rtc_configuration = RTCConfiguration({
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })
    
    # Initialize recorder in session state
    if 'audio_recorder' not in st.session_state:
        st.session_state.audio_recorder = AudioRecorder()
    
    recorder = st.session_state.audio_recorder
    
    # Create WebRTC streamer
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
                "autoGainControl": True,
            }
        },
        async_processing=True,
    )
    
    return webrtc_ctx, recorder

def record_audio_component():
    """Main audio recording component"""
    
    st.markdown("## Voice Recording")
    
    # Create audio recorder
    webrtc_ctx, recorder = create_audio_recorder()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Recording status
        if recorder.recording:
            st.markdown('<div class="recording-status recording-active">🎙️ Recording... Speak now!</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="recording-status recording-inactive">⏸️ Ready to record</div>', 
                       unsafe_allow_html=True)
        
        # Recording controls
        if webrtc_ctx.state.playing:
            if st.button("⏹️ Stop Recording", type="secondary", use_container_width=True):
                recorder.stop_recording()
                webrtc_ctx.stop()
                st.rerun()
        else:
            if st.button("🎙️ Start Recording", type="primary", use_container_width=True):
                recorder.start_recording()
                webrtc_ctx.play()
                st.rerun()
        
        # Display recording status
        if webrtc_ctx.state.playing:
            st.info("Recording is active. Speak clearly into your microphone.")
        elif webrtc_ctx.state.initialized:
            st.success("Microphone connected. Click 'Start Recording' to begin.")
        else:
            st.warning("Please allow microphone access to record audio.")
    
    return recorder

def save_audio_file(audio_data, sample_rate, filename_prefix):
    """Save audio data to a temporary file and return the file path"""
    if audio_data is None or len(audio_data) == 0:
        return None
    
    # Normalize audio data
    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.95
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    sf.write(temp_file.name, audio_data, sample_rate)
    return temp_file.name

def get_audio_duration(audio_data, sample_rate):
    """Calculate the duration of audio data in seconds"""
    if audio_data is None:
        return 0
    return len(audio_data) / sample_rate
