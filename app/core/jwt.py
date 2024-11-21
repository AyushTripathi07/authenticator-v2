import jwt
from datetime import datetime , timedelta , timezone
from config import settings

def generate_jwt(data: dict, expires_in: int=3600):
    payload = data.copy()
    payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)
    return jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm="HS256")


def verify_jwt(token : str):
    try:
        return jwt.decode(token,settings.JWT_SECRET_KEY,algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return ValueError("Token has expired")
    except jwt.InvalidTokenError:
        return ValueError("Invalid token")

