from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
import datetime

class Shift(Base):
    """ Shift """

    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)
    shift_id = Column(String(250), nullable=False)
    shift_name = Column(String(250), nullable=False)
    start_time = Column(String(100), nullable=False)
    end_time = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_created = Column(DateTime, nullable=False)
    incomes = relationship('Income', backref='shift')

    def __init__(self, shift_id, shift_name, start_time, end_time, user_id):
        """ Initializes a shift object"""
        self.shift_id = shift_id
        self.shift_name = shift_name
        self.start_time = start_time
        self.end_time = end_time
        self.user_id = user_id
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a shift object """
        dict = {}
        dict['id'] = self.id
        dict['shift_id'] = self.shift_id
        dict['shift_name'] = self.shift_name
        dict['start_time'] = self.start_time
        dict['end_time'] = self.end_time
        dict['user_id'] = self.user_id
        dict['date_created'] = self.date_created

        return dict