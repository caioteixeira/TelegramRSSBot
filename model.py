from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

import os

Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)


class Feed(Base):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship(Chat)
    url = Column(String(500), nullable=False)


class Model:
    def __init__(self):
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set")

        self.engine = create_engine(os.getenv("DATABASE_URL"))
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def get_chat(self, chat_id):
        chat = self.session.query(Chat).filter(Chat.chat_id == chat_id).one_or_none()
        if chat is None:
            chat = Chat(chat_id=chat_id)
            self.session.add(chat)
        return chat

    def add_feed(self, chat_id, feed_url):
        chat = self.get_chat(chat_id)
        new_feed = Feed(chat=chat, url=feed_url)
        self.session.add(new_feed)
        self.session.commit()

    def get_all_feeds(self):
        return self.session.query(Feed).all()

    def get_feeds(self, chat_id):
        chat = self.get_chat(chat_id)
        return self.session.query(Feed).filter(Feed.chat_id == chat.id).all()
