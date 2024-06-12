from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from .. import database
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/")
def get_posts(db: Session = Depends(database.get_db)):
    my_posts = db.query(models.Posts).all()
    return my_posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    post_query.update(post.model_dump())
    db.commit()

    return post_query.first()
