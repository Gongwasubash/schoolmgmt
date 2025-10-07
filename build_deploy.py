#!/usr/bin/env python
"""
Build and deployment script for the school management system
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    print("🚀 Starting build and deployment process...")
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Continuing despite dependency installation issues...")
    
    # Step 2: Create migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("⚠️  Migration creation failed, but continuing...")
    
    # Step 3: Apply migrations
    if not run_command("python manage.py migrate", "Applying migrations"):
        print("❌ Migration failed - this is critical!")
        return False
    
    # Step 4: Collect static files (if needed)
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Static file collection failed, but continuing...")
    
    print("🎉 Build and deployment process completed!")
    print("🌐 Your application should now be ready to run.")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)