from datetime import datetime

from sqlalchemy.dialects.mysql import TINYINT

from web.core import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.VARCHAR(11), nullable=False)
    nickname = db.Column(db.VARCHAR(32), nullable=False)
    avatar = db.Column(db.VARCHAR(256), default='', comment='头像')
    status = db.Column(TINYINT(2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    posts = db.relationship('Post', backref=db.backref('user'), lazy=True)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64), nullable=False)
    content = db.Column(db.TEXT, comment='内容')
    status = db.Column(TINYINT(2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    location = db.Column(db.JSON, nullable=True, comment='所在位置')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    images = db.relationship('PostImage', backref=db.backref('post'), lazy=True)

    def to_dict(self):
        keys = [x.name for x in self.__table__.columns]
        data = {key: getattr(self, key) for key in keys}
        return data


class PostImage(db.Model):
    __tablename__ = 'post_images'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.VARCHAR(256), nullable=True)
    status = db.Column(TINYINT(2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
