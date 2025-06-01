import subprocess
import os
import sys

def get_resource_path(filename):
    bundle_dir = os.path.abspath(os.path.join(os.path.dirname(sys.executable), '..', 'Resources'))
    return os.path.join(bundle_dir, filename)

run_cmd = get_resource_path("run.command")

# Use AppleScript to open Terminal and run the command
subprocess.call([
    "osascript", "-e",
    f'tell application "Terminal" to do script "chmod +x \\"{run_cmd}\\"; \\"{run_cmd}\\""'
])