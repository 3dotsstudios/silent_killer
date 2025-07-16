from flask import Flask, request, redirect, abort
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

app = Flask(__name__)

AES_KEY = b'ThisIsA32ByteLongSecretKey123456'

@app.route('/')
def index():
    return "💀 Silent Killer server is alive."

@app.route('/favicon.ico')
def favicon():
    return "", 204

@app.route('/r')
def redirect_handler():
    encrypted = request.args.get('l')
    if not encrypted:
        abort(400, "Missing 'l' parameter")

    try:
        encrypted_bytes = base64.urlsafe_b64decode(encrypted)
        iv = encrypted_bytes[:16]
        ciphertext = encrypted_bytes[16:]

        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

        return redirect(decrypted)
    except Exception as e:
        return f"❌ Decryption failed: {str(e)}", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)