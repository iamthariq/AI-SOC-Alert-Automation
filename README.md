# AI-Powered SOC Alert Automation using Wazuh, OpenAI & Telegram

##  Overview
This project simulates a real-world Security Operations Center (SOC) environment by detecting, analyzing, and alerting on multiple cyber attack scenarios.

It integrates Wazuh SIEM with a custom Python detection engine, MITRE ATT&CK mapping, OpenAI-based alert analysis, and Telegram for real-time notifications.

---

##  Architecture

1. Attack Simulation (Kali / Attacker Machine)
2. Logs generated on target system
3. Wazuh collects and stores logs
4. Python script monitors alerts.json
5. Detection engine classifies attacks
6. MITRE ATT&CK mapping applied
7. OpenAI generates AI-based explanation
8. Alerts sent via Telegram Bot

---

##  Attack Scenarios Implemented

### 1. Brute Force Attack (T1110)
Multiple failed SSH login attempts detected.

**Result:**
- Identified repeated login failures
- Attacker IP extracted
- Severity: Medium

---

### 2. Account Compromise (T1110 + T1078)
Successful login after multiple failed attempts.

**Result:**
- Correlated failed + successful login
- Detected as account compromise
- Severity: High


---

### 3. Persistence – New User Creation (T1136)
Unauthorized user added to the system.

**Result:**
- Detected use of adduser
- Classified as persistence mechanism
- Severity: High



---

### 4. Credential Access – /etc/shadow (T1003)
Attempt to access sensitive credential file.

**Result:**
- Detected access attempt (even if failed)
- Classified as credential dumping attempt
- Severity: High


---

### 5. Malware Simulation – EICAR (T1204)
Simulated malware execution using EICAR test file.

**Result:**
- File creation/modification detected
- Classified as malware simulation
- Severity: High


---

## 🤖 AI-Based Alert Analysis

- Integrated OpenAI API to generate SOC-style explanations
- Provides:
  - Attack summary
  - Risk interpretation
  - Recommended actions

---

## 📡 Real-Time Alerting

- Telegram Bot used for instant notifications
- Alerts include:
  - Attack type
  - MITRE mapping
  - Severity
  - Attacker & victim IP
  - AI-generated analysis

---

## 🧠 Key Features

- Real-time log monitoring using Wazuh
- Custom detection engine in Python
- Multi-stage attack correlation
- MITRE ATT&CK framework integration
- AI-powered alert explanation
- Noise reduction using deduplication
- Automated alert delivery via Telegram

---

## 🛠️ Technologies Used

- Wazuh SIEM  
- Python  
- OpenAI API  
- Telegram Bot API  
- Linux (Ubuntu)  
- MITRE ATT&CK Framework  

---

## 🎯 Conclusion

This project demonstrates practical SOC capabilities including threat detection, analysis, and automated response. It simulates real-world attack scenarios and provides intelligent alerting, making it suitable for entry-level SOC Analyst roles.

---
