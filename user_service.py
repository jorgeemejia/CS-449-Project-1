import os
import sys
import json
import datetime
import collections
import contextlib
import logging.config
import sqlite3
import typing
import logging
from datetime import datetime

from fastapi import FastAPI, Depends, Response, HTTPException, status, Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 


ALGORITHM = "pbkdf2_sha256"

class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    user_database: str
    logging_config: str

class UserModel(BaseModel):
    UserID: int
    UserName: str
    PW: str

class UserLoginModel(BaseModel):
    UserName: str
    PW: str    

def get_db():
    with contextlib.closing(sqlite3.connect(settings.user_database)) as db:
        db.row_factory = sqlite3.Row
        yield db


def get_logger():
    return logging.getLogger(__name__)

settings = Settings()
app = FastAPI()

logging.config.fileConfig(settings.logging_config, disable_existing_loggers=False)    

def hash_password(password, salt=None, iterations=260000):
    if salt is None:
        salt = secrets.token_hex(16)
    assert salt and isinstance(salt, str) and "$" not in salt
    assert isinstance(password, str)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
    return "{}${}${}${}".format(ALGORITHM, iterations, salt, b64_hash)


def verify_password(password, password_hash):
    if (password_hash or "").count("$") != 3:
        return False
    algorithm, iterations, salt, b64_hash = password_hash.split("$", 3)
    iterations = int(iterations)
    assert algorithm == ALGORITHM
    compare_hash = hash_password(password, salt, iterations)
    return secrets.compare_digest(password_hash, compare_hash)

def expiration_in(minutes):
    creation = datetime.datetime.now(tz=datetime.timezone.utc)
    expiration = creation + datetime.timedelta(minutes=minutes)
    return creation, expiration


def generate_claims(username, user_id, roles):
    _, exp = expiration_in(20)

    claims = {
        "aud": "krakend.local.gd",
        "iss": "auth.local.gd",
        "sub": username,
        "jti": str(user_id),
        "roles": roles,
        "exp": int(exp.timestamp()),
    }
    token = {
        "access_token": claims,
        "refresh_token": claims,
        "exp": int(exp.timestamp()),
    }

    output = json.dumps(token, indent=4)
    print(output)
    
def generate_keys(key_ids):
    keys = [jwk.JWK.generate(kid=key_id, kty="RSA", alg="RS256") for key_id in key_ids]
    exported_keys = [
        key.export(private_key=private) for key in keys for private in [False, True]
    ]
    keys_as_json = [json.loads(exported_key) for exported_key in exported_keys]
    jwks = {"keys": keys_as_json}
    output = json.dumps(jwks, indent=4)
    print(output)

# Operation/Resource 13
@app.post("/register/", description="Register a new user")
def register_new_user(usermodel: UserModel, db: sqlite3.Connection = Depends(get_db)):
    try:
        # Generate a random salt for each user 
        hashed_password = hash_password(usermodel.PW)
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO users(UserID, UserName, PW) VALUES (?, ?, ?)",
                       (usermodel.UserID, usermodel.UserName, hashed_password))
        db.commit()
        return {"message": "User registration successful"}
    except Exception as e:
        logger.exception("An error occurred during user registration")
        db.rollback()
        raise HTTPException(status_code=500, detail="User registration failed")

# Operation/Resource 14
@app.get("/login/", description="User Login")
def check_user_password(logindata: UserLoginModel, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        hashed_password = cursor.execute("SELECT PW FROM users WHERE UserName=?",(logindata.UserName))
        if (verify_password(logindata.PW, hashed_password)):
            return {"message": "Password verified"}
        else:
            return {"message": "Password mismatch"}
    except Exception as e:   
        logger.exception("An error occurred during password verification")    
        raise HTTPException(status_code=500, detail="Password verification failed") 

@app.get("/test/", description="User Login")
def check_user_password(logindata: UserLoginModel, db: sqlite3.Connection = Depends(get_db)):
    return {"message": "Password mismatch"}