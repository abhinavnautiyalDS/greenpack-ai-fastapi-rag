from pydantic import BaseModel, Field
from typing import Dict

@classmethod
def validate_quantities(cls, value):

    for category, quantity in value.items():

        if quantity < 0:
            raise ValueError(
                f"{category} cannot be negative"
            )

    return value

class SubmitRequest(BaseModel):
    producer_id: str
    month: str = Field(
    ...,
    pattern=r"^\d{4}-\d{2}$"
)
    declared_quantities_kg: Dict[str, float]


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)


