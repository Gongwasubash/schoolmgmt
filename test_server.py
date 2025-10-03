#!/usr/bin/env python
import os
import sys
import django
import subprocess
import time
import requests

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

def test_server():
    print("=== TESTING DJANGO SERVER ===")
    
    try:
        # Test if we can access the pending enquiry page
        response = requests.get('http://127.0.0.1:8000/pending-enquiry/', timeout=5)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"Content length: {len(content)} characters")
            
            # Check for debug information
            if 'Debug Info:' in content:
                print("✓ Debug information found")
            
            # Check for data
            if 'Mike Johnson' in content:
                print("✓ Enquiry data found")
            else:
                print("✗ Enquiry data NOT found")
                
            if 'Carol Davis' in content:
                print("✓ Registration data found")
            else:
                print("✗ Registration data NOT found")
        else:
            print(f"Server returned status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Server is not running. Please start with: python manage.py runserver")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_server()