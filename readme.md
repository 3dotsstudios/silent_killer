# ☠️ Silent Killer - AES Encrypted Redirector

This Flask server securely redirects users from an encrypted URL to a hidden destination using AES-256 encryption. Perfect for stealthy link redirection where the destination must remain obscured.

---

## 🔧 Features

- AES-256-CBC encryption (compatible with your custom encryptor script)
- Supports encrypted links in format:  
  `https://yourdomain.com/r?l=ENCRYPTED_STRING`
- Open-source, lightweight, and deployable on any Python host

---

## 🧠 Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Flask
- pycryptodome

---

## 🚀 Installation

1. **Clone or Download the Project**

```bash
git clone https://github.com/YOUR_USERNAME/silent-killer-redirector.git
cd silent-killer-redirector

pip install -r requirements.txt