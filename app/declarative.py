from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from db import Base, engine


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False, index=True)
    full_name = Column(String)


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)

    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref='posts')

    name = Column(String, nullable=False, index=True)
    text = Column(String, nullable=False)

    published_at = Column(DateTime(timezone=True), server_default=func.now())

    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship('User', backref='posts')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)

    post_id = Column(Integer, ForeignKey('post.id'), index=True, nullable=False)
    post = relationship('Post', backref='comments')

    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship('User', backref='comments')

    published_at = Column(DateTime(timezone=True), server_default=func.now())

    reply_to_id = Column(Integer, ForeignKey('comment.id'))
    reply_to = relationship('Comment', remote_side=[id], backref='sub_comments')


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
