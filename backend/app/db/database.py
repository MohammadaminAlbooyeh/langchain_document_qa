from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# Hardcode the database path for local development
db_path = "sqlite:////Users/amin/Documents/MyProjects/house_finder_bot/backend/data/dev.db"

connect_args = {"check_same_thread": False} if db_path.startswith("sqlite") else {}
engine = create_engine(db_path, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    # import models to register metadata
    from app.models import Base
    from app.models import house, user  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # Add sample data
    _add_sample_data()


def _add_sample_data():
    from app.models.house import House
    from app.models.user import User

    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(House).count() > 0:
            return

        # Create sample user
        user = User(email="admin@example.com", hashed_password="hashedpassword")
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create sample houses with Italian cities
        houses_data = [
            {
                "title": "Modern Apartment in Turin",
                "description": "Beautiful modern apartment in the city center with excellent metro access",
                "price": 1200.0,
                "location": "Turin",
                "bedrooms": 2,
                "bathrooms": 1,
                "area_sqft": 800.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Centro Turin Small Flat",
                "description": "Small 1-room flat in Centro — ideal for testing rooms=1 and district filtering",
                "price": 700.0,
                "location": "Turin",
                "bedrooms": 1,
                "bathrooms": 1,
                "area_sqft": 450.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Cozy Studio in Milan",
                "description": "Charming studio apartment near Duomo",
                "price": 950.0,
                "location": "Milan",
                "bedrooms": 1,
                "bathrooms": 1,
                "area_sqft": 500.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Luxury Villa in Florence",
                "description": "Spacious luxury villa with private garden overlooking the Arno",
                "price": 5000.0,
                "location": "Florence",
                "bedrooms": 4,
                "bathrooms": 3,
                "area_sqft": 2500.0,
                "property_type": "villa",
                "owner_id": user.id
            },
            {
                "title": "Downtown Rome Penthouse",
                "description": "Elegant penthouse with terrace in the heart of Rome",
                "price": 2500.0,
                "location": "Rome",
                "bedrooms": 3,
                "bathrooms": 2,
                "area_sqft": 1400.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Venice Waterfront Apartment",
                "description": "Stunning apartment with canal views in the historic center",
                "price": 3200.0,
                "location": "Venice",
                "bedrooms": 2,
                "bathrooms": 2,
                "area_sqft": 900.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Turin Suburban House",
                "description": "Family house in quiet neighborhood with garden",
                "price": 1800.0,
                "location": "Turin",
                "bedrooms": 3,
                "bathrooms": 2,
                "area_sqft": 1800.0,
                "property_type": "villa",
                "owner_id": user.id
            },
            {
                "title": "Centro Turin Spacious Flat",
                "description": "Comfortable 2-bedroom flat located in Centro area, close to amenities",
                "price": 1400.0,
                "location": "Turin",
                "bedrooms": 2,
                "bathrooms": 1,
                "area_sqft": 850.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Milan Loft",
                "description": "Industrial-style loft in trendy Navigli district",
                "price": 1600.0,
                "location": "Milan",
                "bedrooms": 2,
                "bathrooms": 1,
                "area_sqft": 1100.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Bologna Charming Cottage",
                "description": "Charming cottage near medieval towers",
                "price": 850.0,
                "location": "Bologna",
                "bedrooms": 1,
                "bathrooms": 1,
                "area_sqft": 600.0,
                "property_type": "cottage",
                "owner_id": user.id
            }
        ]

        for house_data in houses_data:
            house = House(**house_data)
            db.add(house)

        db.commit()
    finally:
        db.close()
