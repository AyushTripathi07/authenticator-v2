import secrets
import base64
import hmac
import hashlib
import struct
import time

def generate_totp_secrets(length : int=32)->str:
    """
    Generates a random Base32-encoded secret for TOTP.
    :param length: The length of the random secret (default is 32 bytes).
    :return: A Base32-encoded secret key.
    """

    random_bytes = secrets.token_bytes(length)
    secret = base64.b32encode(random_bytes).decode("UTF-8")
    return secret


def generate_totp(secret: str, time_step: int = 30, digits: int = 6) -> str:
    """
    Generates a TOTP (Time-based One-Time Password).
    :param secret: The shared Base32-encoded secret key.
    :param time_step: The time step in seconds (default is 30).
    :param digits: The number of digits for the OTP (default is 6).
    :return: A TOTP code as a string.
    """
    # Decode the Base32-encoded secret
    key = base64.b32decode(secret, casefold=True)
    
    # Calculate the current time step
    counter = int(time.time()) // time_step

    # Convert the counter to an 8-byte big-endian integer
    counter_bytes = struct.pack(">Q", counter)

    # Generate HMAC-SHA1 hash
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # Perform dynamic truncation
    offset = hmac_hash[-1] & 0x0F
    truncated_hash = hmac_hash[offset:offset + 4]
    code = struct.unpack(">I", truncated_hash)[0] & 0x7FFFFFFF

    # Reduce to the desired number of digits
    otp = code % (10 ** digits)
    return str(otp).zfill(digits)

def validate_totp(secret: str, otp: str, time_step: int = 30, digits: int = 6, tolerance: int = 1) -> bool:
    """
    Validates a TOTP (Time-based One-Time Password).
    :param secret: The shared Base32-encoded secret key.
    :param otp: The OTP to validate.
    :param time_step: The time step in seconds (default is 30).
    :param digits: The number of digits for the OTP (default is 6).
    :param tolerance: The number of time steps to check around the current time (default is 1).
    :return: True if valid, False otherwise.
    """
    
    for i in range(-tolerance, tolerance + 1):
        counter = (int(time.time()) // time_step) + i
        counter_bytes = struct.pack(">Q", counter)
        key = base64.b32decode(secret, casefold=True)
        hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
        offset = hmac_hash[-1] & 0x0F
        truncated_hash = hmac_hash[offset:offset + 4]
        code = struct.unpack(">I", truncated_hash)[0] & 0x7FFFFFFF
        otp_to_check = str(code % (10 ** digits)).zfill(digits)
        if otp_to_check == otp:
            return True
    return False