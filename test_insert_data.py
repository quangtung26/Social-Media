from sqlalchemy.orm import Session
from app.database import engine
from app.models import Posts, User
from app.main import *
from app import schemas
from app.router.user import create_user

# Create a new session
session = Session(bind=engine)

my_posts = [
    # {"title": "Post 1", "content": "Content 1"},
    # {"title": "favourite foold", "content": "I like pizza "},
]

users = [{"id": 1, "email": "tung1@gmail.com", "password": "123456"},
         {"id": 2, "email": "tung12@gmail.com", "password": "tung123"}]

# Create new Posts instances for each post
for post in my_posts:
    new_post = Posts(title=post["title"], content=post["content"])
    session.add(new_post)

for user in users:
    user = schemas.UserCreate(**user)
    create_user(user, session)

# Commit the session to save the objects in the database
session.commit()

# Close the session
session.close()