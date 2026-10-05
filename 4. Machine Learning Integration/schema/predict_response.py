from pydantic import BaseModel, computed_field, Field
from typing import Annotated, Literal

class Prediction_response(BaseModel):

    Health_Score : float = Field(..., description='The predicted mental health score', examples=4.56)