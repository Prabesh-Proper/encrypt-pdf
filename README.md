# 🔐 Secure PDF Encryptor / Decryptor

A simple and secure Flask-based web application that allows users to
encrypt and decrypt PDF files using strong AES-256 encryption.

This tool helps protect sensitive PDFs from unauthorized access and
reduces the risk of interception (e.g., Man-in-the-Middle attacks).

------------------------------------------------------------------------

## 🚀 Features

-   🔒 AES-256 (CBC mode) encryption\
-   🔑 PBKDF2 key derivation with 100,000 iterations\
-   🧂 Random salt per file\
-   🎲 Random IV (Initialization Vector) per encryption\
-   💾 In-memory processing (no files stored on server)\
-   🖥️ Clean and modern web UI\
-   🔓 One-click encryption & decryption

------------------------------------------------------------------------

## 🛠️ Technologies Used

-   Python 3
-   Flask
-   Cryptography (hazmat primitives)

------------------------------------------------------------------------

## 📦 Installation

### 1️⃣ Clone the Repository

``` bash
git clone https://github.com/Prabesh-Proper/encrypt-pdf.git
cd secure-pdf-encryptor
```

### 2️⃣ Create Virtual Environment (Recommended)

``` bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

``` bash
pip install flask cryptography
```

------------------------------------------------------------------------

## ▶️ Run the Application

``` bash
python app.py
```

Then open your browser and go to:

http://127.0.0.1:5000

------------------------------------------------------------------------

## 🔐 How It Works

### Encryption Process

1.  User uploads a PDF.
2.  User enters a password.
3.  A random 16-byte salt is generated.
4.  The password is processed using:
    -   PBKDF2
    -   SHA-256
    -   100,000 iterations
5.  AES-256 key is derived.
6.  Data is padded using PKCS7.
7.  File is encrypted using AES-CBC.
8.  Final output structure:

\[salt (16 bytes)\] + \[IV (16 bytes)\] + \[encrypted data\]

------------------------------------------------------------------------

### Decryption Process

1.  Extract salt and IV from file.
2.  Derive key using same password.
3.  Decrypt AES-CBC.
4.  Remove PKCS7 padding.
5.  Return original PDF.

------------------------------------------------------------------------

## 🛡️ Security Notes

-   Files are never stored on the server.
-   All processing is done in memory.
-   Strong password is recommended (minimum 8+ characters).
-   If a wrong password is entered, decryption will fail.
-   This tool is intended for secure local usage.

------------------------------------------------------------------------

## ⚠️ Limitations

-   No user authentication system.
-   No HTTPS (use behind reverse proxy for production).
-   Not resistant to brute-force attacks if weak passwords are used.
-   Debug mode is enabled by default (disable for production).

To disable debug mode:

``` python
app.run(debug=False)
```

------------------------------------------------------------------------

## 🌍 Future Improvements

-   Add drag & drop support\
-   Add password strength meter\
-   Add file size validation\
-   Add HTTPS configuration guide\
-   Add Docker support\
-   Add rate limiting for brute-force protection

------------------------------------------------------------------------

## 📜 License

This project is open-source and free to use for educational and personal
purposes.

------------------------------------------------------------------------

## 👨‍💻 Author

Created as a cybersecurity learning project to demonstrate:

-   Secure key derivation
-   AES encryption implementation
-   Secure file handling in web applications
