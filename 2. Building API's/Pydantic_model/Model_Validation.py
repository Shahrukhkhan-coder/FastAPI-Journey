from pydantic import BaseModel, StrictInt, Field
from typing import Optional, Annotated


class Student(BaseModel):

    id : Annotated[int, Field(..., gt=0, title='Student_ID')]
    Name : Annotated[str, Field(..., max_length=20, title='Student Name')]
    Age : Annotated[Optional[StrictInt], Field(gt=0, title='Student Age')]
    Department : Annotated[str, Field(..., max_length=20, title='Student Department')]


