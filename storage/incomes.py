from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
import datetime

class Income(Base):
    """ Income """

    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True)
    income_id = Column(String(250), nullable=False)
    income_amount = Column(Integer, nullable=False)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, income_id, income_amount, shift_id):
        """ Initializes an income object"""
        self.income_id = income_id
        self.shift_id = shift_id
        self.income_amount = income_amount
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of an income object """
        dict = {}
        dict['id'] = self.id
        dict['income_id'] = self.income_id
        dict['income_amount'] = self.income_amount
        dict['shift_id'] = self.shift_id
        dict['date_created'] = self.date_created

        return dict