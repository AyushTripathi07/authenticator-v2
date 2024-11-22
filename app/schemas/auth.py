from pydantic import BaseModel , EmailStr, Field

class SignupRequest(BaseModel):
    """
    Schema for the signup request.
    """
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    password: str = Field(..., min_length=8, example="SecurePassword123")
    email: EmailStr = Field(..., example="john.doe@example.com")


class LoginRequest(BaseModel):
    """
    Schema for the login request.
    """
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    password: str = Field(..., min_length=8, example="SecurePassword123")
    otp: str = Field(..., min_length=6, max_length=6, example="123456")  

class QRCodeRequest(BaseModel):
    username: str