"""
Security Automation Pipeline
Runs OWASP ZAP scans, generates reports, opens findings,
and uploads artifacts to AWS S3 for centralized security reporting.
"""
import subprocess
import os
import sys
from datetime import datetime, UTC
import urllib.request
import urllib.error
import webbrowser
import boto3

# Project Configuration
TARGET_URL = "http://host.docker.internal:5000"
LOCAL_TARGET_URL = "http://localhost:5000"
REPORT_DIR = os.path.join(os.getcwd(), "zap-reports")
REPORT_FILE = "zap-report.html"

def log(message):
    """Pipeline-style logging with timestamps"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_flask_running():
    """Check if the flask app is reachable before running the scan."""
    log(f"Checking if flask app is reachable at {LOCAL_TARGET_URL}...")

    try:
        with urllib.request.urlopen(LOCAL_TARGET_URL, timeout=3) as response:
            if response.status == 200:
                log("Flask app is running and reachable. ")
                return True
            else:
                log(f"Flask responded with unexpected status code: {response.status}")
                return False
    except (urllib.error.URLError, TimeoutError) as e:
        log(f"Flask app is NOT reachable on {LOCAL_TARGET_URL}, Reason: {e}")
        return False

def check_docker():
    """Verify Docker is installed and running"""
    log("Checking Docker availability...")
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL)
        log("Docker is installed and accessible.")
    except subprocess.CalledProcessError:
        log("ERROR: Docker is not available. Please start Docker Desktop.")
        sys.exit(1)

def run_zap_scan():
    """Run OWASP ZAP Baseline Scan using Docker"""
    log("Starting OWASP ZAP Security Scan...")

    docker_command = [
        "docker", "run", "--rm",
        "-v", f"{REPORT_DIR}:/zap/wrk",
        "-t", "ghcr.io/zaproxy/zaproxy:stable",
        "zap-baseline.py",
        "-t", TARGET_URL,
        "-r", REPORT_FILE
    ]

    results = subprocess.run(docker_command, check=False)
    if results.returncode == 0:
        log("ZAP scan completed successfully. (exit code 0).")

    else:
        log("Zap scan completed with warnings/findings (non-zero exit code).")

        log(f"Security report generated at:{os.path.join(REPORT_DIR, REPORT_FILE)}")
        return results.returncode


def open_report():
    """Open the generated ZAP HTML report in the default browser"""
    report_path = os.path.join(REPORT_DIR, REPORT_FILE)
    abs_path = os.path.abspath(report_path)

    if os.path.exists(abs_path):
        log(f"Opening report: {abs_path}")
        webbrowser.open(f"file:///{abs_path}")
    else:
        log(f"WARNING: Report not found, Cannot open: {abs_path}")

def upload_zap_report_to_s3():
    """Uploads report to s3 bucket, with timestamp for security automation audit tracking."""
    bucket ="kevin-devsecops-security-pipeline-reports"
    report_path = r"C:\Users\kevin\security-automation-zap-pipeline\zap-reports\zap-report.html"

    if not os.path.exists(report_path):
        raise FileNotFoundError(f"ZAP report not found at {report_path}")

    s3 = boto3.client("s3")

    #keep runs organized in s3
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
    key = f"zap-reports/{timestamp}/zap-report.html"

    s3.upload_file(report_path, bucket, key)
    print(f" ZAP report uploaded to s3://{bucket}/{key}")



def main():
    """Orchestrate the pipeline: prep reports, validate Docker + target app,
    run OWASP ZAP, and exit with status."""
    log("=== DevSecOps Security Automation Pipeline Started ===")

    # Ensure report directory exists
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        log("Created zap-reports directory.")

    check_docker()
    #NEW: Validate target application is running
    if not check_flask_running():
        log("PIPELINE STOPPED: Flask app is not running on http://localhost:5000")
        log("Please start the flask app (py app\\app.py) and try again.")
        sys.exit(1)

    run_zap_scan()

    log("ZAP scan completed.  Attempting to open report...")
    log("DEBUG: About to open report...")

    open_report()
    upload_zap_report_to_s3()

    log("DEBUG:Finished open_report() call.")
    log("=== Security Pipeline Completed Successfully ===")

if __name__ == "__main__":
    main()