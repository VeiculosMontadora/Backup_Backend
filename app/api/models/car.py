from pydantic import BaseModel
from typing import Optional

# Car model.
#
# This model represents a car object in the database.
# Add any fields that you want to store in the database.


class Car(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
