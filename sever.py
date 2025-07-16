from flask import Flask, request, redirect, abort
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

app = Flask(__name__)

AES_KEY = b'ThisIsA32ByteLongSecretKey123456'  # Must match encryptor

@app.route('/r')
def redirector():
    encrypted = request.args.get('l')
    if not encrypted:
        return abort(400, "Missing encrypted link")

    try:
        data = base64.urlsafe_b64decode(encrypted)
        iv = data[:16]
        ciphertext = data[16:]

        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        url = decrypted.decode('utf-8')

        # Security check
        if not url.startswith(("http://", "https://")):
            return abort(400, "Invalid URL")

        return redirect(url)
    except Exception as e:
        return f"❌ Decryption error: {str(e)}", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)