# Data Notes Demo

This demo showcases data sonification techniques, including voice transformation and interactive mapping with audio visualization.

## Features

### 1. Voice Transformation Demo
- Record your voice while observing a waveform
- Experience how data patterns can transform speech
- Compare original and transformed audio
- View pitch analysis visualizations

### 2. SNAP Retailer Audio Map
- Interactive map of King County SNAP retailer locations
- Audio sonification of store types by zip code
- Each store type mapped to different musical instruments
- Click zip codes to hear unique "sound signatures"

## Quick Start

### Option 1: Use the Python Server Script (Recommended)
```bash
python run_demo_server.py
```
This will:
- Start a local server on port 8000
- Automatically open your browser to the demo
- Handle CORS issues and proper MIME types

### Option 2: Manual Server Setup
```bash
# Navigate to this directory
cd /path/to/DataNotes

# Start a Python HTTP server
python -m http.server 8000

# Open your browser to:
# http://localhost:8000/demo.html
```

### Option 3: Using Node.js (if available)
```bash
# Install a simple HTTP server
npm install -g http-server

# Start the server
http-server -p 8000

# Open your browser to:
# http://localhost:8000/demo.html
```

## Important Notes

⚠️ **Browser Security**: Modern browsers block local file access for security reasons. You **must** use a local web server to run this demo.

⚠️ **Audio Context**: The audio features require user interaction to start (browser security policy). Click any audio button to enable audio functionality.

## File Structure

```
DataNotes/
├── demo.html                 # Main demo file
├── run_demo_server.py        # Python server script
├── DEMO_README.md           # This file
├── MapData/
│   └── SNAP Retailer Location data KING county.csv
├── Music/
│   ├── Cymatics - Cedar - 95 BPM C# Min Bass.wav
│   ├── Cymatics - Cedar - 95 BPM C# Min Guitar.wav
│   ├── Cymatics - Cedar - 95 BPM C# Min Lead.wav
│   ├── Cymatics - Overtime - 95 BPM C# Min Pad.wav
│   ├── Cymatics - Overtime - 95 BPM C# Min Piano.wav
│   ├── Cymatics - Overtime - 95 BPM C# Min Synth.wav
│   ├── Cymatics - Ablaze Drum Loop - 95 BPM Kick.wav
│   ├── Cymatics - Ablaze Drum Loop - 95 BPM Snare.wav
│   ├── Cymatics - Ablaze Drum Loop - 95 BPM Hihat.wav
│   └── Cymatics - Ablaze Drum Loop - 95 BPM Open Hat.wav
```

## Audio Instrument Mapping

The SNAP map uses the following instrument mapping:

| Store Type | Instrument(s) |
|------------|---------------|
| Grocery Store | Bass |
| Convenience Store | Guitar |
| Supermarket | Lead |
| Super Store | Pad |
| Farmers and Markets | Piano + Synth |
| Specialty Store | Kick + Snare |
| Other | Hihat + Open Hat |

## Troubleshooting

### "Unable to load map data" Error
- Make sure you're running the demo through a web server (not opening the HTML file directly)
- Check that the CSV file exists in the MapData folder
- Try refreshing the page

### Audio Not Playing
- Click any audio button first to enable the audio context
- Check that your browser allows audio playback
- Ensure audio files are present in the Music folder

### Map Not Loading
- Verify that all files are in the correct locations
- Check browser console for specific error messages
- Try a different browser

## Data Sources

- **SNAP Data**: USDA SNAP Retailer website (August 20, 2025)
- **Audio Samples**: Cymatics (royalty-free music samples)

## Browser Compatibility

This demo works best with modern browsers:
- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## License

This demo is for educational purposes. The audio samples are from Cymatics and are royalty-free for educational use.
