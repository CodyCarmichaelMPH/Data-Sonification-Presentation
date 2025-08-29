#!/usr/bin/env python3
"""
Deploy DataNotes demo to existing GitHub repository
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 DataNotes GitHub Deployment Helper")
    print("=" * 50)
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed. Please install Git first.")
        return
    
    # Check if we're in the right directory
    if not os.path.exists("demo.html"):
        print("❌ demo.html not found. Please run this script from the DataNotes directory.")
        return
    
    # Initialize git repository (if not already done)
    if not os.path.exists(".git"):
        print("📁 Initializing Git repository...")
        if not run_command("git init", "Initializing Git repository"):
            return
    
    # Add all files
    if not run_command("git add .", "Adding all files to Git"):
        return
    
    # Check if there are changes to commit
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("ℹ️  No changes to commit. All files are up to date.")
        return
    
    # Commit changes
    commit_message = "Update DataNotes demo with interactive map and audio sonification"
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        return
    
    # Check if remote exists
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "origin" not in result.stdout:
        print("🔗 Adding remote repository...")
        remote_url = "https://github.com/CodyCarmichaelMPH/Data-Sonification-Presentation.git"
        if not run_command(f"git remote add origin {remote_url}", "Adding remote repository"):
            return
    
    # Push to GitHub
    print("📤 Pushing to GitHub...")
    if not run_command("git push -u origin main", "Pushing to GitHub"):
        # Try master branch if main doesn't exist
        if not run_command("git push -u origin master", "Pushing to GitHub (master branch)"):
            return
    
    print("\n🎉 Deployment completed successfully!")
    print("=" * 50)
    print("🌐 Your live demo will be available at:")
    print("   https://codycarmichaelmph.github.io/Data-Sonification-Presentation/")
    print("\n📝 Next steps:")
    print("   1. Go to your GitHub repository")
    print("   2. Go to Settings → Pages")
    print("   3. Select 'Deploy from a branch'")
    print("   4. Choose 'main' or 'master' branch and '/(root)' folder")
    print("   5. Click Save")
    print("\n⏱️  It may take a few minutes for the site to be live.")

if __name__ == "__main__":
    main()
