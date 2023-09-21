from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from botocore.exceptions import NoCredentialsError
import boto3, os
import requests
from fastapi.responses import JSONResponse  # Add this import
from dotenv import load_dotenv

load_dotenv("./.env")

app = FastAPI()
# Configure CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS Cognito configuration
COGNITO_REGION = os.getenv("COGNITO_REGION")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"

# Initialize the AWS Cognito client
cognito = boto3.client("cognito-idp", region_name=COGNITO_REGION)

# Define a Pydantic model for JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

# OAuth2 Password Bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to get the current user's groups from Cognito JWT
def get_user_groups(token: str = Depends(oauth2_scheme)):
    try:
        unverified_claims = jwt.get_unverified_claims(token)
        groups = unverified_claims.get("cognito:groups", [])
        return groups
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Home route
@app.get("/")
def read_root():
    return {"message": "OK"}


@app.post("/grant-access")
async def grant_access(
    authorization: str = Header(None),
    username: str = Header(None)
):
    try:
        # Check if the authorization header is present (you can replace this check with your actual authorization logic)
        if authorization is None:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        # Use the `username` directly in your backend logic
        # For example, add the user to the "admin" group
        cognito.admin_add_user_to_group(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username=username,
            GroupName="admin"
        )

        return {"message": "Permission granted!"}

    except HTTPException as e:
        raise e



# Route to check access to a protected resource
@app.get("/cat")
def check_access(groups: str = Depends(get_user_groups)):
    if "admin" not in groups:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this operation.")
    return {"message": "You are authorized to perform this operation."}


