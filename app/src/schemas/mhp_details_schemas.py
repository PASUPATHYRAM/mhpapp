from pydantic import BaseModel,validators,field_validator, Field
from typing import Optional, List
import math



class Id_schema(BaseModel):
    id: int

class MhpAddress_schema(BaseModel):
    address_line1: str
    address_line2: str

class MhpDetails_schema(BaseModel):
    parkname: str
    address: MhpAddress_schema
    city: str
    state: str
    zip: int

    @field_validator('state')
    @classmethod
    def state_validate(cls,state):
        return state.upper()

    @field_validator('zip')
    @classmethod
    def zip_lengthcheck(cls,zip):
        if len(str(zip))!=5:
            raise ValueError("Zip should be of length")
        else:
            return zip


class Graph(BaseModel):
    title: str
    xlable: str
    ylable: str
    sort_ord: Optional[str]

    @field_validator('sort_ord')
    def sort_order_validaotr(cls,v):
        if v is None or v.lower().startswith('a'):
            return 'asc'
        elif v.lower().startswith('d'):
            return 'desc'
        elif v.lower().startswith('b'):
            return 'bell'
        else:
            raise ValueError("Invalid sort type")

class MhpContact_schema(BaseModel):
    address_fk: str
    website: Optional[str]
    contact_person: Optional[str]=Field(default=None)
    email: Optional[str]
    phone: Optional[str]=Field(None,title='Enter the phone sep by -',examples=['123-345-8790'])

    # @field_validator('email')
    # def email_check(cls,value):
    #     if str(value).endswith('.com'):
    #         return value
    #     else:
    #         raise ValueError("Invalid email id")
    @field_validator('contact_person','email','website','phone')
    def contact_person_chk(cls,value):
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return None
        else:
            return value

class Contacts_schema(BaseModel):
    contact_person: str
    website: str
    email: str
    phone: str


class ParkDetails_Contact(BaseModel):
    park_details: MhpDetails_schema
    contacts: Contacts_schema


class Records(BaseModel):
    New_records: int
    Old_records: int

class Stat_Records(BaseModel):
    Stat:List[Records]

class Response_model(BaseModel):
    Data_added_status: Stat_Records

class Response_model_park_pdf(BaseModel):
    parkname: str
    city: str
    state: str
    zip: int
    address:MhpAddress_schema

class UserRegisterSchema(BaseModel):
    name: str
    password: str
    admin: bool



