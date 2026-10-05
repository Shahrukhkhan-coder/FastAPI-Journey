from pydantic import BaseModel, computed_field, Field, model_validator
from typing import Annotated, Literal
from fastapi import HTTPException


class User_data(BaseModel):

    Age                     : Annotated[int, Field(..., gt=0, le=150, description='Age of  the user')]
    Gender                  : Literal['Male', 'Female', 'Other']
    Country                 : Literal['Other', 'Canada', 'USA', 'India','Australia','UK','Germany']
    Academic_Level          : Literal['Undergraduate', 'Graduate', 'High School']
    Most_Used_Platform      : Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter','YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp','WeChat']
    Purpose_Of_Use          : Literal['Networking', 'Education', 'Entertainment', 'News']
    Avg_Daily_Usage_Hours   : Annotated[int, Field(..., gt=0, le=24, description='Mobile daily usage hours of the user')]
    Daily_Unlocks           : Annotated[int, Field(..., gt=0, le=500, description='Mobiles daily unlocks count of the user')]
    Study_Hours             : Annotated[int, Field(..., gt=0, le=24, description='Daily study hours of the user')]
    Physical_Activity_Hours : Annotated[int, Field(..., gt=0, le=24, description='Daily Physical Activity hours of the user')]
    Sleep_Hours_Per_Night   : Annotated[int, Field(..., gt=0, le=24, description='Daily sleep  of the user')]
    Stress_Level            : Literal['Medium', 'Low', 'Very High', 'High']


    @model_validator(mode='after')
    def valid_total_hours(cls, model):
        total = model.Avg_Daily_Usage_Hours + model.Study_Hours + model.Physical_Activity_Hours + model.Sleep_Hours_Per_Night

        if total > 24:
            raise HTTPException(status_code=400, detail=f'Total of study hours + activity hours +sleep hours + Avg daily use mobile hours cannot exceed 24 hours. Got {total}')

        return model