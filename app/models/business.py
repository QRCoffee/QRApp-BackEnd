from typing import Optional

from beanie import Insert, Link, before_event
from pydantic import Field
from pymongo import IndexModel

from .base import Base


class BusinessType(Base):
    name: str = Field(..., description="Unique business type name")
    description: Optional[str] = Field(default=None, description="Optional description")

    class Settings:
        indexes = [
            IndexModel([("name", 1)], unique=True)
        ]

    @before_event(Insert)
    def upper_name(self):
        self.name = self.name.upper()


class Business(Base):
    name: str = Field(..., description="Unique business name")
    address: str = Field(..., description="Business address (street, city, country, postal_code)")
    contact: str = Field(..., description="Contact info (phone, email, website)")
    business_type: Link[BusinessType]
    tax_code: Optional[str] = Field(default=None, description="Business tax code")
    owner: Optional["Link[User]"] = Field(description="Business Owner") # type: ignore

    class Settings:
        indexes = [
            IndexModel([("name", 1)], unique=True)
        ]