import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Booking, ContactMessage, Testimonial, User, Product

app = FastAPI(title="Cleaning Services API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Cleaning Services Backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db as test_db
        if test_db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = test_db.name if hasattr(test_db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = test_db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Schemas endpoint (used by viewer tools)
@app.get("/schema")
def get_schema():
    return {
        "collections": [
            "user", "product", "booking", "contactmessage", "testimonial"
        ]
    }

# Public API endpoints

@app.post("/api/bookings")
def create_booking(payload: Booking):
    try:
        booking_id = create_document("booking", payload)
        return {"success": True, "id": booking_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/testimonials")
def list_testimonials(limit: int = 6):
    try:
        docs = get_documents("testimonial", {}, limit)
        # Convert ObjectId to string for JSON
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def contact_message(payload: ContactMessage):
    try:
        message_id = create_document("contactmessage", payload)
        return {"success": True, "id": message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
