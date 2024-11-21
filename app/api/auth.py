from fastapi import FastAPI , APIRouter , HTTPException
from fastapi.responses import StreamingResponse
from models.user import User
from core.security import hash_password , verfiy_password
from core.jwt import generate_jwt
from schemas.auth import SignupRequest , LoginRequest
from core.totp import generate_totp_secrets
from core.totp import validate_totp
from core.qr_code import generate_qr_code

users_db = {}
router = APIRouter()

@router.post("/signup")
def signup(request: SignupRequest):
    if request.username in users_db:
        raise HTTPException(status_code=400,detail="Username Already Exists")
    hashed_password = hash_password(request.password)
    secret = generate_totp_secrets() 

    users_db[request.username] = User(username=request.username,
                                      hashed_password=hashed_password,
                                      secret_key=secret)
    
    return {"message" : "User Created Successfully" , "username": request.username, "totp_secret" : secret}
    
@router.post("/signin")
def login(request: LoginRequest):
    user = users_db.get(request.username)
    if not user or not verfiy_password(request.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalied Credential")
    
    if not validate_totp(user.secret_key, request.otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    token = generate_jwt({"username": user.username})
    return {"access_token":token,"token_type":"bearer","db" : users_db}

@router.get("/generate-qr-code", response_class=StreamingResponse)
def get_qr_code(username: str):
    """
    Generates a QR code for a user's TOTP secret.
    :param username: The username of the user.
    :return: StreamingResponse containing the QR code image.
    """
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.secret_key:
        raise HTTPException(status_code=400, detail="TOTP secret not configured for this user")

    # Generate QR code as bytes
    qr_code_bytes = generate_qr_code(user.secret_key, username)

    # Wrap the QR code bytes in a BytesIO stream for StreamingResponse
    return StreamingResponse(
        content=iter([qr_code_bytes]),  # Wrap in an iterable
        media_type="image/png",
    )
