"""
AI-Powered SOC Alert Automation (Wazuh + Telegram + OpenAI)

Description:
Monitors Wazuh alerts, detects attack patterns, maps to MITRE ATT&CK,
generates AI explanations, and sends alerts to Telegram.

Security:
Uses environment variables for API keys (no hardcoding).
"""

import json
import time
import requests
import re
import os
from openai import OpenAI

================= CONFIG =================

ALERT_FILE = "/var/ossec/logs/alerts/alerts.json"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

================= TELEGRAM =================

def send_telegram(message):
if not TELEGRAM_TOKEN or not CHAT_ID:
print("⚠️ Telegram not configured")
return

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
try:
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})
except Exception as e:
    print(f"Telegram Error: {e}")

================= IP EXTRACTION =================

def extract_source_ip(full_log):
patterns = [
r'from (\d+.\d+.\d+.\d+)',
r'srcip=(\d+.\d+.\d+.\d+)',
r'client (\d+.\d+.\d+.\d+)'
]

for pattern in patterns:
    match = re.search(pattern, full_log)
    if match:
        return match.group(1)

return None

================= GLOBAL TRACKERS =================

failed_attempts = {}
recent_alerts = set()

================= DETECTION ENGINE =================

def detect_attack(alert):
full_log = alert.get("full_log", "").lower()
rule_desc = alert.get("rule", {}).get("description", "").lower()

ip = extract_source_ip(full_log)

# 1. Malware Detection (EICAR)
if "eicar" in full_log or "eicar" in rule_desc:
    return "Malware Detected"

# 2. Persistence (User Creation)
elif "adduser" in full_log or "useradd" in full_log:
    return "Persistence - New User"

# 3. Credential Access
elif "/etc/shadow" in full_log:
    return "Credential Access"

# 4. Brute Force Tracking
elif "failed password" in full_log:
    if ip:
        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
    return "Brute Force Attempt"

# 5. Successful Login / Account Compromise
elif "accepted password" in full_log or "session opened for user" in full_log:

    # Correlation → compromise
    if ip and failed_attempts.get(ip, 0) >= 2:
        failed_attempts[ip] = 0
        return "Account Compromise"

    # Reset counter after success
    if ip:
        failed_attempts[ip] = 0

    return "Successful Login"

return None

================= MITRE =================

def map_mitre(attack):
mapping = {
"Brute Force Attempt": "T1110 - Brute Force (Initial Access)",
"Account Compromise": "T1110 + T1078 (Initial Access)",
"Successful Login": "T1078 - Valid Accounts (Initial Access)",
"Persistence - New User": "T1136 - Create Account (Persistence)",
"Credential Access": "T1003 - Credential Dumping",
"Malware Detected": "T1204 - User Execution"
}
return mapping.get(attack, "N/A")

================= SEVERITY =================

def get_severity(attack):
if attack in [
"Malware Detected",
"Credential Access",
"Persistence - New User",
"Account Compromise",
"Successful Login"
]:
return "High"

elif attack == "Brute Force Attempt":
    return "Medium"

return "Low"

================= AI EXPLANATION =================

def get_ai_explanation(attack, log):
if not OPENAI_API_KEY:
return "AI analysis disabled"

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a SOC analyst. Explain the alert in 2 lines with a recommendation."},
            {"role": "user", "content": f"Attack: {attack}\nLog: {log}"}
        ],
        max_tokens=80
    )
    return response.choices[0].message.content.strip()
except:
    return "AI analysis unavailable"

================= MAIN MONITOR =================

def monitor():
print("🚀 SOC Monitoring Started...")

try:
    with open(ALERT_FILE, "r") as f:
        f.seek(0, 2)

        while True:
            line = f.readline()

            if not line:
                time.sleep(1)
                continue

            try:
                alert = json.loads(line)
            except:
                continue

            # Deduplication
            alert_id = alert.get("id")
            if alert_id in recent_alerts:
                continue
            recent_alerts.add(alert_id)

            attack = detect_attack(alert)

            if attack is None:
                continue

            full_log = alert.get("full_log", "")
            attacker_ip = extract_source_ip(full_log)
            victim_ip = alert.get("agent", {}).get("ip", "Unknown")

            mitre = map_mitre(attack)
            severity = get_severity(attack)

            if attack in [
                "Brute Force Attempt",
                "Account Compromise",
                "Malware Detected",
                "Credential Access",
                "Persistence - New User"
            ]:
                ai_text = get_ai_explanation(attack, full_log)
            else:
                ai_text = "Normal activity"

            message = f"""

🚨 SOC ALERT 🚨

Attack: {attack}
MITRE: {mitre}
Severity: {severity}

Attacker IP: {attacker_ip if attacker_ip else "Local Activity"}
Victim IP: {victim_ip}

AI Analysis:
{ai_text}
"""

            print(message)
            send_telegram(message)

except FileNotFoundError:
    print("❌ Wazuh alert file not found")

================= RUN =================

if name == "main":
monitor()