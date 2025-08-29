# DataNotes - Interactive Data Sonification Demo

An innovative web application that demonstrates data sonification through interactive mapping and audio visualization of King County SNAP retailer data.

## 🌐 Live Demo

**[View the live demo here](https://codycarmichaelmph.github.io/Data-Sonification-Presentation/)**

## 🎯 Features

### 🗺️ Interactive Choropleth Map
- **King County Zip Code Visualization**: Complete coverage of all King County zip codes
- **SNAP Retailer Data**: Color-coded polygons showing store density (white to purple gradient)
- **Real-time Interaction**: Click zip codes to see detailed store information
- **Geographic Accuracy**: Uses official King County zip code boundaries from GeoJSON data

### 🎵 Audio Sonification
- **Data-to-Sound Mapping**: Each store type corresponds to specific musical instruments
- **Dynamic Audio Generation**: More stores = more instruments playing simultaneously
- **Interactive Audio Controls**: Play individual zip codes or all tracks together
- **7 Instrument Categories**:
  - **Drums**: Hihat + Open Hat, Snare + Kick
  - **Bass**: C# Minor Bass
  - **Guitar**: C# Minor Guitar
  - **Lead**: C# Minor Lead
  - **Pads**: C# Min Pad
  - **Piano**: C# Min Piano
  - **Synth**: C# Min Synth

### 📊 Voice Analysis & Waveform Visualization
- **Real-time Recording**: Capture and analyze voice data
- **Waveform Display**: Visual representation of audio data
- **Data Transformation**: Apply mathematical transformations to audio
- **Interactive Charts**: Plotly.js powered visualizations

## 🚀 Quick Start

### Local Development
1. **Clone the repository**:
   ```bash
   git clone https://github.com/CodyCarmichaelMPH/Data-Sonification-Presentation.git
   cd Data-Sonification-Presentation
   ```

2. **Start the local server**:
   ```bash
   python run_demo_server.py
   ```

3. **Open your browser**:
   Navigate to `http://localhost:8000/demo.html`

### GitHub Pages Deployment
The demo is automatically deployed to GitHub Pages when you push to the main branch.

## 📁 Project Structure

```
DataNotes/
├── demo.html                 # Main demo application
├── index.html               # Landing page for GitHub Pages
├── run_demo_server.py       # Local development server
├── MapData/                 # Geographic and SNAP data
│   ├── SNAP Retailer Location data KING county.csv
│   └── Zipcodes_for_King_County_and_Surrounding_Area_(Shorelines)___zipcode_shore_area.geojson
├── Music/                   # Audio files for sonification
│   ├── Cymatics - Ablaze Drum Loop - 95 BPM Hihat.wav
│   ├── Cymatics - Cedar - 95 BPM C# Min Bass.wav
│   └── ... (10 total audio files)
├── .github/workflows/       # GitHub Actions deployment
│   └── deploy.yml
└── README.md               # This file
```

## 🛠️ Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Mapping**: Leaflet.js for interactive maps
- **Visualization**: Plotly.js for charts and graphs
- **Audio**: Web Audio API for real-time audio processing
- **Data**: CSV parsing, GeoJSON handling
- **Deployment**: GitHub Pages with GitHub Actions

## 📊 Data Sources

- **SNAP Retailer Data**: USDA SNAP Retailer website (August 20, 2025)
- **Zip Code Boundaries**: King County GIS data
- **Audio Samples**: Cymatics music production samples (95 BPM, C# Minor)

## 🎮 How to Use

### Map Interaction
1. **Explore the Map**: Hover over zip codes to see boundaries
2. **Click Zip Codes**: View detailed store information and play audio
3. **Audio Controls**: Use the sidebar to play all tracks or stop audio
4. **Legend**: Reference the color scale to understand store density

### Audio Sonification
1. **Individual Zip Codes**: Click any zip code and press "Play Audio"
2. **All Tracks**: Use "Play All Tracks Together" to hear all instruments
3. **Stop Controls**: Use "Stop All Audio" or individual stop buttons
4. **Audio Categories**: Each store type triggers specific instruments

### Voice Analysis
1. **Record Audio**: Click the record button to capture your voice
2. **View Waveform**: See real-time visualization of your audio
3. **Transform Data**: Apply mathematical transformations
4. **Compare Results**: View before/after waveform comparisons

## 🔧 Customization

### Adding New Audio Files
1. Place new WAV files in the `Music/` directory
2. Update the `instrumentFiles` object in `demo.html`
3. Modify the `storeTypeMapping` to assign instruments to store types

### Modifying the Map
1. Replace the GeoJSON file with new boundary data
2. Update the `loadKingCountyZipBoundaries()` function
3. Modify color schemes in `getSNAPZipCodeColor()`

### Adding New Data Sources
1. Update the CSV parsing in `parseSNAPCSV()`
2. Modify the data processing in `processSNAPDataByZipCode()`
3. Update the popup content generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **USDA SNAP Program** for retailer location data
- **King County GIS** for geographic boundary data
- **Cymatics** for high-quality audio samples
- **Leaflet.js** and **Plotly.js** communities for excellent mapping and visualization libraries

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for data visualization and sonification research**
