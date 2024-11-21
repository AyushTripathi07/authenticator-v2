from fastapi import FastAPI
from api import auth
app = FastAPI(title = "Authenticator-v2")

@app.get("/")
def read_root():
    return {"message": "Welcome to the TOTP Authenticator API!"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
