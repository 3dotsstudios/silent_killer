import base64
import urllib.parse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# ====== CONFIG ======
# 32-byte AES key (must match your Flask redirector's key)
AES_KEY = b'ThisIsA32ByteLongSecretKey123456'  # 32 bytes for AES-256
# ====================

def encrypt_link(link: str) -> str:
    iv = get_random_bytes(16)  # Random IV
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(link.encode('utf-8'), AES.block_size))
    encrypted = iv + ciphertext
    return base64.urlsafe_b64encode(encrypted).decode('utf-8')

def generate_href(domain: str, encrypted: str) -> str:
    domain = domain.strip().rstrip('/')
    return f'href="{domain}/r?l={urllib.parse.quote_plus(encrypted)}"'

def main():
    print("🔐 Silent Killer — Encrypter")

    # Step 1: Ask for your redirect domain
    domain = input("🌍 Enter your full domain (e.g. https://login.yourdomain.com): ").strip()

    # Step 2: Ask for the real target link
    original_url = input("🔗 Enter the link to encrypt (e.g. https://real-destination.com): ").strip()

    # Step 3: Encrypt it
    encrypted = encrypt_link(original_url)

    # Step 4: Output final href
    final_href = generate_href(domain, encrypted)
    print("\n✅ Encrypted HTML href (use in <a> tags):\n")
    print(final_href)

if __name__ == "__main__":
    main()