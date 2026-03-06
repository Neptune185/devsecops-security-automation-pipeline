# Cloud-Integrated DevSecOps Security Automation Pipeline

## Overview

This project demonstrates a cloud-integrated DevSecOps security automation pipeline using:

- Python
- OWASP ZAP (Docker)
- Flask test application
- AWS S3 for report storage
- Automated HTML report generation
- Timestamped cloud uploads for traceability

The pipeline simulates a real-world DevSecOps workflow where security testing is automated and security artifacts are centrally stored in cloud infrastructure.

---
## Architecture

![DevSecOps Pipeline](docs/devsecops-security-pipeline-architecture.png)

1. Flask application runs locally
2. OWASP ZAP runs via Docker
3. Python automation script triggers security scan
4. HTML security report generated
5. Report uploaded to AWS S3
6. Reports organized by timestamp

---

## Technologies Used

- Python 3.13
- OWASP ZAP Docker
- Flask
- AWS CLI
- boto3
- Git / GitHub
- VS Code

---

## How It Works

1. Start Docker
2. Launch Flask app
3. Execute automation script
4. Generate ZAP security report
5. Automatically upload report to AWS S3 bucket

---

## Cloud Security Implementation

- IAM user authentication
- Secure AWS credential configuration
- S3 bucket with structured report storage
- Timestamp-based folder organization
- Programmatic S3 uploads using boto3

---

## Sample Output

ZAP scan generates:
- PASS findings
- WARN findings
- HTML report artifact
- Cloud upload confirmation

Example:


---

## Why This Project Matters

This project demonstrates:

- Security automation integration
- Infrastructure + application security alignment
- Cloud-native security artifact management
- DevSecOps workflow orchestration
- Real-world CI/CD security foundation

---

## Future Enhancements

- GitHub Actions CI integration
- Automated scan on push
- S3 lifecycle policies
- AWS CloudWatch logging
- Terraform-based infrastructure provisioning
