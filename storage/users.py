from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
import datetime

class User(Base):
    """ User """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    user_name = Column(String(250), nullable=False)
    password = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    shifts = relationship("Shift", backref='user')

    def __init__(self, user_id, user_name, password):
        """ Initializes a user object"""
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a user object """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['user_name'] = self.user_name
        dict['password'] = self.password
        dict['date_created'] = self.date_created

        return dict