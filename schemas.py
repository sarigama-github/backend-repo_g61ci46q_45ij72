"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Cleaning Services App Schemas

class Booking(BaseModel):
    """Bookings collection schema. Collection: "booking""" 
    name: str = Field(..., description="Customer full name")
    email: EmailStr = Field(..., description="Customer email")
    phone: str = Field(..., description="Customer phone number")
    address: str = Field(..., description="Service address")
    service_type: str = Field(..., description="Requested service type")
    date: str = Field(..., description="Preferred date (ISO string or human text)")
    time: str = Field(..., description="Preferred time window")
    notes: Optional[str] = Field(None, description="Additional notes")
    source: Optional[str] = Field("website", description="Lead source")

class ContactMessage(BaseModel):
    """Contact messages from contact form. Collection: "contactmessage""" 
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    message: str = Field(..., description="Message body")
    phone: Optional[str] = Field(None, description="Optional phone")
    subject: Optional[str] = Field(None, description="Subject")

class Testimonial(BaseModel):
    """Testimonials left by customers. Collection: "testimonial"""
    name: str = Field(..., description="Customer name")
    rating: int = Field(..., ge=1, le=5, description="Star rating 1-5")
    comment: str = Field(..., description="Testimonial text")
    city: Optional[str] = Field(None, description="City or area")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
