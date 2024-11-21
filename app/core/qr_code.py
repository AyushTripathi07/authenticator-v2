import qrcode
from io import BytesIO

def generate_qr_code(secret: str, username: str, issuer: str = "TOTP-App") -> bytes:
    """
    Generate a QR code for TOTP setup.
    :param secret: The Base32-encoded TOTP secret.
    :param username: The username to associate with the TOTP.
    :param issuer: The name of the application (e.g., "TOTP-App").
    :return: QR code image in bytes format (PNG).
    """
    # Create the otpauth:// URI
    uri = f"otpauth://totp/{issuer}:{username}?secret={secret}&issuer={issuer}"
    
    # Generate the QR code
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(uri)
    qr.make(fit=True)

    # Save QR code to a byte stream
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()