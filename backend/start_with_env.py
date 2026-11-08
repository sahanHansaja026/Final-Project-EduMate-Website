import os
# Set the database URL explicitly
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres123@localhost:5432/edumate?sslmode=disable'

# Now run uvicorn
import subprocess
import sys

# Note: log file handling optional

proc = subprocess.Popen(
    [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000'],
    cwd='C:\\Users\\sahan\\Documents\\GitHub\\Final-Project-EduMate-Website\\backend',
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print(f"Backend started with PID: {proc.pid}")
print("Waiting for server to start...")
import time
time.sleep(3)

# Check if process is still running
if proc.poll() is None:
    print("✅ Backend server is running")
else:
    print("❌ Backend failed to start")
    print(f"stderr: {proc.stderr.read().decode()}")