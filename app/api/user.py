import uuid
from http import HTTPStatus

from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_encryption_key
from app.api.utils import add_row_to_table
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserSchema

admin = APIRouter()


@admin.post("/user", response_model=UserSchema, status_code=HTTPStatus.CREATED)
def create_user(
    user: UserCreateSchema,
    db: Session = Depends(get_db()),
    encryption_key: bytes = Depends(get_encryption_key),
):
    """
    This endpoint is created only for development purposes.
    In production environment, user info should be stored in other services, for example Keycloak.
    So that's why this endpoint is not even tested.
    """
    fernet = Fernet(encryption_key)
    user.password = fernet.encrypt(user.password.encode()).decode()
    return add_row_to_table(db, User(**user.dict() | {"id": uuid.uuid4()}))


@admin.get("/user", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db())):
    return db.query(User).all()
