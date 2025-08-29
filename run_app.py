#!/usr/bin/env python3
"""
Simple launcher for the Data Notes Streamlit application
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Change to the script directory
        os.chdir(script_dir)
        
        # Launch Streamlit
        print("🚀 Launching Data Notes...")
        print("📊 Voice Waveform Transformation App")
        print("=" * 50)
        
        # Run streamlit with the app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_realtime.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("💡 Make sure you have installed the requirements:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
