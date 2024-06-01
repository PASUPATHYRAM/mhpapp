# It contains only the MH park details

from sqlalchemy import Column,Integer,String,func,ForeignKey
from app.src.db_setup import Base
from sqlalchemy.orm import validates,relationship
from sqlalchemy.ext.hybrid import hybrid_property


class MhpDetails(Base):
    __tablename__='park_details'
    id=Column(Integer,autoincrement=True,index=True)
    park_name=Column(String)
    address_line_1=Column(String,primary_key=True)
    address_line_2=Column(String)
    city=Column(String)
    state=Column(String(2))
    zip=Column(Integer)

    park_details_rel=relationship('Mhpcontact',back_populates='park_contact_rel')

    @validates('state')
    def state_convert(self,key,state):
        return state.upper()

    @hybrid_property
    def derived_col(self):
        return self.park_name +'-'+ self.city
    @derived_col.expression
    def derived_col(cls):
        return func.concat(cls.park_name,'-',cls.city)

class Mhpcontact(Base):
    __tablename__="park_contact"
    id=Column(Integer,primary_key=True,autoincrement=True)
    address_fk=Column(String,ForeignKey('park_details.address_line_1'))
    website=Column(String,nullable=True)
    contact_person=Column(String,nullable=True)
    email=Column(String,nullable=True)
    phone=Column(String,nullable=True)
    park_contact_rel=relationship('MhpDetails',back_populates='park_details_rel')

    @validates('contact_person')
    def contact_person_check(self,key,contact_person):
        return contact_person.title()
    @validates('phone')
    def phone_check(self,key,phone):
        if phone:
            if len(str(phone))==12:
                return phone
            else:
                raise "Invalid phone number"

class UserRegister(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pass_hash = Column(String, nullable=False)
    admin = Column(Boolean, default=False)

    def hasing_pass(self, value):
        self.pass_hash = pbkdf2_sha256.hash(value)





