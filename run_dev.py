#!/usr/bin/env python3
"""
Development server with auto-restart functionality
"""
import subprocess
import time
import os
import signal
import sys

def run_server():
    """Run the Dash server"""
    try:
        print("Starting Dash server...")
        process = subprocess.Popen(['python', 'app_dash.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

def main():
    print("Development server with auto-restart")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    process = None
    
    try:
        while True:
            if process is None or process.poll() is not None:
                if process:
                    print("Server stopped, restarting...")
                process = run_server()
                if process:
                    print("Server started at http://localhost:8050")
                    print("Make changes to app_dash.py and the server will restart automatically")
                    print("-" * 50)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nStopping server...")
        if process:
            process.terminate()
            process.wait()
        print("Server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main() 