import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.utils import add_row_to_table
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserSchema

admin = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@admin.post("/", response_model=UserSchema, status_code=HTTPStatus.CREATED)
async def create_user(
    user: UserCreateSchema,
    db: Session = Depends(get_db()),
):
    user.password = pwd_context.hash(user.password)
    return add_row_to_table(db, User(**user.dict() | {"id": uuid.uuid4()}))


@admin.get("/", response_model=list[UserSchema])
async def get_users(db: Session = Depends(get_db())):
    return db.query(User).all()
