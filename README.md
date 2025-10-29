# ☁️ AWS Cloud Automation and Monitoring using Python & Boto3

## 📌 Project Overview
This project automates AWS resource management and security auditing using **Python** and **Boto3**.  
It performs **EC2 provisioning**, **S3 bucket creation**, **IAM access key audits**, and **CPU utilization monitoring** using **CloudWatch** — all from a single Python script.

---

## ⚙️ Features
- 🚀 **EC2 Instance Creation** – Automatically creates EC2 instances.
- 🪣 **S3 Bucket Automation** – Creates and validates S3 buckets.
- 👤 **IAM Audit** – Detects IAM users with access keys older than 90 days.
- 🔒 **Security Group Check** – Finds open ports (SSH/RDP) for potential security risks.
- 📊 **CloudWatch Monitoring** – Tracks EC2 CPU utilization and logs high-usage alerts.
- 🧾 **Logging** – Records all audit results with timestamps.

---

## 🧰 Tech Stack
| Component | Technology |
|------------|-------------|
| Programming Language | Python |
| Cloud Platform | AWS |
| AWS Services Used | EC2, S3, IAM, CloudWatch |
| Library | Boto3 |
| Others | Logging, JSON, Datetime |

---

## 🧑‍💻 Setup Instructions

### Prerequisites
- AWS account
- Python 3.x installed
- AWS credentials configured (`aws configure`)

### Installation Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/aws-cloud-automation-monitoring.git

# AWS-cloud-automation
Automating AWS Services (EC2, S3, IAM, CloudWatch) using Python and Boto3
Test commit