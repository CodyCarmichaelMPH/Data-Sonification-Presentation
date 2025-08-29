# Upload Instructions for Large Files

Due to the large size of the GeoJSON file (34+ MB), the automatic push is failing. Here's how to upload your files to GitHub:

## Option 1: GitHub Web Interface (Recommended)

1. **Go to your repository**: https://github.com/CodyCarmichaelMPH/Data-Sonification-Presentation

2. **Click "Add file" → "Upload files"**

3. **Drag and drop these files/folders**:
   - `demo.html` (main demo file)
   - `index.html` (landing page)
   - `README.md` (documentation)
   - `DEPLOYMENT.md` (deployment guide)
   - `deploy_to_github.py` (deployment script)
   - `run_demo_server.py` (local server)
   - `MapData/` folder (contains CSV and GeoJSON)
   - `Music/` folder (contains audio files)
   - `.github/workflows/deploy.yml` (GitHub Actions)

4. **Add commit message**: "Add DataNotes demo with interactive map and audio sonification"

5. **Click "Commit changes"**

## Option 2: Use Git LFS for Large Files

If you prefer command line, we can set up Git LFS:

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.geojson"
git lfs track "*.wav"

# Add .gitattributes
git add .gitattributes

# Commit and push
git add .
git commit -m "Add DataNotes demo with LFS for large files"
git push -u origin master
```

## Option 3: Split the GeoJSON File

We could create a smaller version of the GeoJSON file with only essential data.

## After Upload

Once files are uploaded:

1. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Select "Deploy from a branch"
   - Choose "master" branch and "/(root)" folder
   - Click Save

2. **Your site will be live at**:
   ```
   https://codycarmichaelmph.github.io/Data-Sonification-Presentation/
   ```

## File Structure

Your repository should contain:
```
Data-Sonification-Presentation/
├── demo.html                 # Main demo application
├── index.html               # Landing page
├── README.md               # Documentation
├── DEPLOYMENT.md           # Deployment guide
├── deploy_to_github.py     # Deployment script
├── run_demo_server.py      # Local server
├── MapData/                # Geographic data
│   ├── SNAP Retailer Location data KING county.csv
│   └── Zipcodes_for_King_County_and_Surrounding_Area_(Shorelines)___zipcode_shore_area.geojson
├── Music/                  # Audio files
│   └── [10 WAV files]
└── .github/workflows/      # GitHub Actions
    └── deploy.yml
```

## Troubleshooting

- **Large file errors**: Use Option 1 (web interface) or Option 2 (Git LFS)
- **SSL errors**: Try again later or use web interface
- **Timeout errors**: Use web interface for large files

The web interface is the most reliable method for uploading large files to GitHub.
