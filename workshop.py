import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator

UUIDstr = str

class User(BaseModel):
    id: UUIDstr
    name = 'John Doe'
    age: Optional[int] = None
    email: EmailStr
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

    @validator('id')
    def id_must_contain_be_valid_uuid(cls, v):
        # this will raise value error which is what we want!
        return uuid.UUID(v)

external_data = {
    'id': '2f38f65a-0911-e511-80d0-005056966c6a',
    'signup_ts': '2021-06-01 12:22',
    'email': "fred@formatics.nl",
    'friends': [1, 2, '3'],
}

user = User(**external_data)
print(user.id)
#> 2f38f65a-0911-e511-80d0-005056966c6a
print(repr(user.signup_ts))
#> datetime.datetime(2021, 6, 1, 12, 22)
print(user.friends)
#> [1, 2, 3]
print(user.dict())
"""
{
'id': '2f38f65a-0911-e511-80d0-005056966c6a', 
'age': None, 
'email': 'fred@formatics.nl', 
'signup_ts': datetime.datetime(2021, 6, 1, 12, 22), 
'friends': [1, 2, 3], 
'name': 'John Doe'
}
"""