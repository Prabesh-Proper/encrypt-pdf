from flask import Flask, request, send_file, render_template_string
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import io
import base64

app = Flask(__name__)

# Simple HTML UI
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure PDF Encryptor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h2 {
            color: #333;
            margin-bottom: 30px;
        }
        input[type="file"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box;
        }
        input[type="file"] {
            padding: 10px;
        }
        input[type="password"]:focus, input[type="file"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn-group {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }
        button {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .btn-encrypt {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-decrypt {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
        .security-info {
            margin-top: 30px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            font-size: 12px;
            color: #666;
        }
        .security-info h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .security-info ul {
            margin: 0;
            padding-left: 20px;
        }
        .security-info li {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔐 Secure PDF Encryptor / Decryptor</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf" required>
            <input type="password" name="password" placeholder="Enter password" required minlength="4">
            <div class="btn-group">
                <button name="action" value="encrypt" class="btn-encrypt">🔒 Encrypt PDF</button>
                <button name="action" value="decrypt" class="btn-decrypt">🔓 Decrypt PDF</button>
            </div>
        </form>
        <div class="security-info">
            <h4>🛡️ Security Features</h4>
            <ul>
                <li>AES-256 strong encryption</li>
                <li>100,000 PBKDF2 iterations</li>
                <li>Random salt + IV per file</li>
                <li>All processing in memory</li>
                <li>No file stored on server</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(data, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return salt + iv + encrypted

def decrypt_file(data, password):
    salt = data[:16]
    iv = data[16:32]
    encrypted = data[32:]

    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        password = request.form["password"]
        action = request.form["action"]

        file_data = file.read()

        try:
            if action == "encrypt":
                output_data = encrypt_file(file_data, password)
                filename = "encrypted.pdf"
            else:
                output_data = decrypt_file(file_data, password)
                filename = "decrypted.pdf"

            return send_file(
                io.BytesIO(output_data),
                as_attachment=True,
                download_name=filename,
                mimetype="application/pdf"
            )

        except Exception as e:
            return "❌ Error: Wrong password or corrupted file."

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(debug=True)
