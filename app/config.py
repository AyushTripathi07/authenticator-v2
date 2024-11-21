import os
from constants import JWT_SECRET_KEY , TOTP_DIGITS , TOTP_INTERVAL
class Settings:
    JWT_SECRET_KEY = JWT_SECRET_KEY
    TOTP_INTERVAL = TOTP_INTERVAL
    TOTP_DIGITS = TOTP_DIGITS

settings = Settings()
