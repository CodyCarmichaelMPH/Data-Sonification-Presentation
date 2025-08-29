"""
Configuration file for Data Notes application

This file contains various settings that can be customized to modify
the behavior and appearance of the Data Notes application.
"""

# Audio Settings
AUDIO_CONFIG = {
    "sample_rate": 44100,  # Audio sample rate in Hz
    "channels": 1,         # Number of audio channels (1 = mono, 2 = stereo)
    "modulation_strength": 0.3,  # Strength of waveform modulation (0.0 to 1.0)
    "max_duration": 30,    # Maximum recording duration in seconds
}

# Visualization Settings
VISUALIZATION_CONFIG = {
    "graph_height": 400,   # Height of the main data graph in pixels
    "audio_vis_height": 150,  # Height of audio waveform visualizations
    "line_width": 3,       # Width of the main graph line
    "fill_opacity": 0.1,   # Opacity of the graph fill area
    "grid_color": "lightgray",  # Color of grid lines
}

# Data Generation Settings
DATA_CONFIG = {
    "num_points": 100,     # Number of points in the sample data
    "time_range": 10,      # Time range for the x-axis
    "noise_level": 0.1,    # Level of random noise in the data
    "frequencies": [1.0, 2.0, 0.5],  # Frequencies for the composite waveform
    "amplitudes": [0.5, 0.3, 0.2],   # Amplitudes for each frequency component
}

# UI Settings
UI_CONFIG = {
    "page_title": "Data Notes - Data Sonification",
    "page_icon": "🎵",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "main_color": "#1f77b4",  # Primary color for the application
    "secondary_color": "#666",  # Secondary color for text
}

# WebRTC Settings
WEBRTC_CONFIG = {
    "ice_servers": [{"urls": ["stun:stun.l.google.com:19302"]}],
    "media_constraints": {
        "video": False,
        "audio": {
            "sampleRate": 44100,
            "channelCount": 1,
            "echoCancellation": True,
            "noiseSuppression": True,
            "autoGainControl": True,
        }
    }
}

# File Settings
FILE_CONFIG = {
    "temp_dir": None,      # Temporary directory for audio files (None = system default)
    "audio_format": "wav",  # Audio format for saved files
    "filename_prefix": "datanotes",  # Prefix for saved audio files
}

# Advanced Settings
ADVANCED_CONFIG = {
    "enable_debug": False,  # Enable debug mode with additional logging
    "cache_audio": True,    # Cache audio data in session state
    "auto_normalize": True,  # Automatically normalize audio levels
    "prevent_clipping": True,  # Prevent audio clipping during modulation
}
