from .base import Base
from pydantic import Field
from beanie import Link
from typing import Optional
from app.models.business import Business

class Branch(Base):
    name: str = Field(..., description="Unique business name")
    address: str = Field(..., description="Business address (street, city, country, postal_code)")
    contact: str = Field(..., description="Contact info (phone, email, website)")
    business: Link[Business]