# GitHub Pages Deployment Guide

This guide will help you deploy your DataNotes demo to GitHub Pages for public access.

## 🚀 Quick Deployment Steps

### 1. Use Existing GitHub Repository

You already have a repository at: [https://github.com/CodyCarmichaelMPH/Data-Sonification-Presentation](https://github.com/CodyCarmichaelMPH/Data-Sonification-Presentation)

This repository is already set up and ready for deployment!

### 2. Upload Your Files

#### Option A: Using GitHub Web Interface
1. In your new repository, click "uploading an existing file"
2. Drag and drop all files from your local `DataNotes` folder
3. Commit the changes

#### Option B: Using Git Command Line
```bash
# Navigate to your DataNotes folder
cd path/to/DataNotes

# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Update DataNotes demo with interactive map and audio sonification"

# Add remote repository
git remote add origin https://github.com/CodyCarmichaelMPH/Data-Sonification-Presentation.git

# Push to GitHub
git push -u origin main
```

#### Option C: Using the Deployment Script
```bash
# Run the automated deployment script
python deploy_to_github.py
```

### 3. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Pages** section (in the left sidebar)
4. Under **Source**, select **Deploy from a branch**
5. Choose **main** branch and **/(root)** folder
6. Click **Save**

### 4. Configure GitHub Actions (Optional)

The `.github/workflows/deploy.yml` file will automatically deploy your site when you push changes.

To enable it:
1. Go to **Settings** → **Actions** → **General**
2. Under **Actions permissions**, select **Allow all actions and reusable workflows**
3. Click **Save**

### 5. Access Your Live Site

Your site will be available at:
```
https://codycarmichaelmph.github.io/Data-Sonification-Presentation/
```

**Note**: It may take a few minutes for the first deployment to complete.

## 🔧 Custom Domain (Optional)

If you want to use a custom domain:

1. In **Settings** → **Pages**
2. Under **Custom domain**, enter your domain
3. Click **Save**
4. Add a CNAME record pointing to `[your-username].github.io`

## 📝 Update README

Don't forget to update the README.md file:
1. Replace `[your-username]` with your actual GitHub username
2. Replace `[your-repo-name]` with your actual repository name
3. Update the live demo link

## 🐛 Troubleshooting

### Common Issues

**Site not loading:**
- Check that the repository is public
- Verify GitHub Pages is enabled in Settings
- Wait a few minutes for deployment

**Audio not working:**
- GitHub Pages serves over HTTPS, which is required for audio
- Check browser console for CORS errors
- Ensure all audio files are properly uploaded

**Map not displaying:**
- Verify all files in `MapData/` folder are uploaded
- Check browser console for file loading errors
- Ensure GeoJSON file is accessible

### File Size Limits

GitHub has file size limits:
- Individual files: 100MB max
- Repository: 1GB recommended
- Large files: Consider using Git LFS

## 🔄 Updating Your Site

To update your live site:

1. Make changes to your local files
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. GitHub Actions will automatically redeploy

## 📊 Analytics (Optional)

To track site usage:

1. Go to **Settings** → **Pages**
2. Check **Google Analytics** if you have a tracking ID
3. Or use GitHub's built-in traffic analytics in **Insights** tab

## 🎯 Next Steps

Once deployed, you can:
- Share the live URL with others
- Add more features and push updates
- Customize the landing page
- Add more data sources
- Implement additional audio features

---

**Your DataNotes demo is now live and accessible to anyone with an internet connection!** 🌐
