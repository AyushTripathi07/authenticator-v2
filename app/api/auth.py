from fastapi import FastAPI , APIRouter , HTTPException
from fastapi.responses import StreamingResponse
from models.user import User
from core.security import hash_password , verfiy_password
from core.jwt import generate_jwt
from schemas.auth import SignupRequest , LoginRequest , QRCodeRequest
from core.totp import generate_totp_secrets
from core.totp import validate_totp
from core.qr_code import generate_qr_code
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import SessionLocal
from models.user import User

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Database error: {e}") 
        raise
    finally:
        db.close()


router = APIRouter()

@router.post("/signup")
def signup(request: SignupRequest , db:Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == request.username).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="Username Already Exists")
    hashed_password = hash_password(request.password)
    secret = generate_totp_secrets() 

    new_user = User(
        username=request.username,
        hashed_password=hashed_password,
        secret_key=secret
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # return {"message" : "User Created Successfully" , "username": request.username, "totp_secret" : secret}
    return {"message" : "User Created Successfully" , "username": request.username}

    
@router.post("/signin")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verfiy_password(request.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalied Credential")
    
    if not validate_totp(user.secret_key, request.otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    token = generate_jwt({"username": user.username})
    return {"access_token":token,"token_type":"bearer"}

@router.post("/generate-qr-code", response_class=StreamingResponse)
def get_qr_code(request:QRCodeRequest ,db: Session = Depends(get_db)):
    """
    Generates a QR code for a user's TOTP secret.
    :param username: The username of the user.
    :return: StreamingResponse containing the QR code image.
    """
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with username '{request.username}' not found"
        )
    
    if not user.secret_key:
        raise HTTPException(
            status_code=400, 
            detail="TOTP secret error"
        )

    # Generate QR code as bytes
    qr_code_bytes = generate_qr_code(user.secret_key, request.username)

    # Wrap the QR code bytes in a BytesIO stream for StreamingResponse
    return StreamingResponse(
        content=iter([qr_code_bytes]),  # Wrap in an iterable
        media_type="image/png",
    )
