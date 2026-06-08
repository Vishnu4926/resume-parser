from fastapi import APIRouter
from database.connection import SessionLocal

from schemas.user_schema import (
    UserCreate,
    UserLogin
)

from database.user_crud import (
    get_user_by_email,
    create_user
)

from auth.password_handler import (
    hash_password,
    verify_password
)

from auth.jwt_handler import (
    create_access_token
)

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    try:

        existing_user = get_user_by_email(
            db,
            user.email
        )

        if existing_user:

            return {
                "message": "Email already registered"
            }

        hashed_password = hash_password(
            user.password
        )

        new_user = create_user(
            db,
            user.username,
            user.email,
            hashed_password
        )

        return {
            "message": "User created successfully",
            "user_id": new_user.id
        }

    finally:
        db.close()

@router.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    try:

        db_user = get_user_by_email(
            db,
            user.email
        )

        if not db_user:

            return {
                "message": "Invalid credentials"
            }

        valid_password = verify_password(
            user.password,
            db_user.password
        )

        if not valid_password:

            return {
                "message": "Invalid credentials"
            }

        token = create_access_token(
            {
                "sub": db_user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        db.close()
