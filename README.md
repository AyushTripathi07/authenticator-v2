# Authenticator-v2

A Python-based authentication system that includes TOTP-based two-factor authentication (2FA) functionality. This project allows users to sign up, log in, and generate QR codes for TOTP setup, leveraging FastAPI, PostgreSQL, and Python's cryptographic libraries.

---

## Features

- **User Registration and Login**:
  - Secure password hashing using `bcrypt`.
  - JWT-based token authentication.

- **TOTP-Based Two-Factor Authentication**:
  - Generates TOTP secrets and QR codes for users.
  - Verifies TOTP codes during login.

- **Database Integration**:
  - PostgreSQL used for storing user data securely.

---

## Requirements

- Python 3.10+
- PostgreSQL
- Pip (Python Package Manager)

---

## Installation

TODO
python3 -c "from db.init_db import init_db; init_db()"
