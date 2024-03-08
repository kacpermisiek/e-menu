from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.menu import Menu
from app.schemas.menu import MenuSchema

admin = APIRouter()
public = APIRouter()


@public.get("/", response_model=List[MenuSchema])
def get_menus(db: Session = Depends(get_db())):
    return db.query(Menu).all()
