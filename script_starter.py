import threading
import subprocess
import signal
import sys
import os

# Define the paths to the scripts you want to run
script1 = 'log_saver.py'
# script2 = 'python_tester.py'
script3 = 'TW423L_to_lof_file.py'

# List to keep track of the subprocesses
subprocesses = []

# Function to run a script in a subprocess
def run_script(script):
    try:
        proc = subprocess.Popen([sys.executable, script])
        subprocesses.append(proc)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, script, output=stdout, stderr=stderr)
    except Exception as e:
        print(f"Error running {script}: {e}")
        stop_all_threads()
        sys.exit(1)

# Function to stop all threads and subprocesses
def stop_all_threads():
    for proc in subprocesses:
        if proc.poll() is None:  # If the process is still running
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    print("All subprocesses terminated.")
    sys.exit(0)

# Signal handler for graceful termination
def signal_handler(sig, frame):
    print('Caught interrupt signal. Terminating all processes.')
    stop_all_threads()

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Create and start threads
threads = []
for script in [script1, script3]: # script2 was deleted from here --> python_tester.py 
    thread = threading.Thread(target=run_script, args=(script,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()
