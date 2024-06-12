from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import utils
from .. import models, schemas
from .. import database

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # hash the password - user.password
    user.password = utils.hash(user.password)

    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} not found")

    return user