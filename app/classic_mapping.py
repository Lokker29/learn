from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Table, func
from sqlalchemy.orm import registry, relationship

from db import engine

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

category_table = Table(
    'category', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True, index=True, nullable=False)
)


class Category:
    pass


user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('nickname', String, nullable=False, index=True),
    Column('full_name', String)
)


class User:
    pass


post_table = Table(
    'post', metadata,
    Column('id', Integer, primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), nullable=False),
    Column('name', String, nullable=False, index=True),
    Column('text', String, nullable=False),
    Column('published_at', DateTime(timezone=True), server_default=func.now()),
    Column('author_id', Integer, ForeignKey('user.id'), nullable=False)
)


class Post:
    pass


comment_table = Table(
    'comment', metadata,
    Column('id', Integer, primary_key=True),
    Column('post_id', Integer, ForeignKey('post.id'), index=True, nullable=False),
    Column('author_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('published_at', DateTime(timezone=True), server_default=func.now()),
    Column('reply_to_id', Integer, ForeignKey('comment.id')),
)


class Comment:
    pass


mapper_registry.map_imperatively(Category, category_table)
mapper_registry.map_imperatively(User, user_table)
mapper_registry.map_imperatively(Post, post_table, properties={
    'category': relationship('Category', backref='posts'),
    'author': relationship('User', backref='posts')
})
mapper_registry.map_imperatively(Comment, comment_table, properties={
    'post': relationship('Post', backref='comments'),
    'author': relationship('User', backref='comments'),
    'reply_to': relationship('Comment', remote_side=[comment_table.c.id], backref='sub_comments')
})


if __name__ == '__main__':
    metadata.drop_all(engine)
    metadata.create_all(engine)
