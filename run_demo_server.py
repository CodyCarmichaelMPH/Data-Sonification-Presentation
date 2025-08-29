#!/usr/bin/env python3
"""
Simple HTTP server for running the Data Notes demo locally.
This script starts a local web server to serve the demo.html file and related assets.
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Set up the server
    PORT = 8000
    
    # Create a custom handler that serves files with proper MIME types
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers to allow local file access
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def guess_type(self, path):
            # Ensure proper MIME types for our files
            if path.endswith('.csv'):
                return 'text/csv'
            elif path.endswith('.wav'):
                return 'audio/wav'
            return super().guess_type(path)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Starting local server at http://localhost:{PORT}")
            print(f"📁 Serving files from: {script_dir}")
            print(f"🌐 Open your browser to: http://localhost:{PORT}/demo.html")
            print("\n📋 Available files:")
            
            # List available files
            for file_path in script_dir.glob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    print(f"   - {file_path.name}")
            
            print("\n⏹️  Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Try to open the browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}/demo.html')
                print("🌐 Browser opened automatically!")
            except:
                print("⚠️  Could not open browser automatically. Please open manually.")
            
            # Start the server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Please try a different port or stop the existing server.")
            print("💡 You can specify a different port by modifying the PORT variable in this script.")
        else:
            print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
