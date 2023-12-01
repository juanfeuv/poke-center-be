import traceback

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from app.api.v1.deps import get_current_user
from app.core.oauth.hashing import verify, bcrypt
from app.core.oauth.jwttoken import create_access_token
from app.database.crud.crud_users import CRUDUsers
from app.api.v1.global_import import FastApiResponse
from pydantic import BaseModel


router = APIRouter()


class User(BaseModel):
    username: str
    password: str


class Password(BaseModel):
    password: str


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    try:
        user = CRUDUsers.get_by_username(username=request.username)
        user_id = user.id
        if not user:
            raise HTTPException(status_code=400,
                                detail=f'No user found with this {request.username} username')
        if not verify(request.password, user["password"]):
            raise HTTPException(status_code=400,
                                detail=f'Wrong Username or password')
        data = {"username": user["username"],
                "user_id": str(user_id)
                }
        access_token = create_access_token(data=data)
        return {"access_token": access_token, "token_type": "bearer", "username": user["username"]}
    except Exception as e:
        print(f"error {e}")
        return FastApiResponse.failure(str(e))


@router.post('/change-user-password')
def change_user_password(password: Password, current_user=Depends(get_current_user)):

    try:
        user_id = current_user.get("user_id")
        hashed_pass = bcrypt(password.password)
        CRUDUsers.update_password(user_id, user_id, hashed_pass)

        return FastApiResponse.successful

    except Exception as e:
        print(f"Error: {e}", traceback.format_exc())
        return FastApiResponse.failure(str(e))


@router.post('/create-user')
def create_user(user: User):
    try:
        hashed_pass = bcrypt(user.password)
        if CRUDUsers.user_already_exist(user.username):
            raise Exception("Username Already Exist")
        CRUDUsers.create_object(username=user.username,
                                password=hashed_pass)
        return FastApiResponse.successful
    except Exception as e:
        print(f"Error: {e}", traceback.format_exc())
        return FastApiResponse.failure(str(e))
