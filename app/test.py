from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine

from classic_mapping import Comment, Post, User, Category
# from declarative import Comment, Post, User, Category

session = Session(engine, autocommit=True)


category = Category(name='Science')
session.add(category)

user = User(nickname='Lokker')
session.add(user)

post = Post(author=user, category=category, name='Super post', text='Some text')
session.add(post)

post = Post(author=user, category=category, name='Another post', text='Another text')
session.add(post)

result = session.execute(select(Post, User).join(Post.author))

for post, user in result.all():
    print(post, post.id, post.name)
    print(user, user.id, user.nickname)
    print()
