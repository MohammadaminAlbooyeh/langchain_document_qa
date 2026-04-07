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

        # Create sample houses
        houses_data = [
            {
                "title": "Modern Apartment",
                "description": "Beautiful modern apartment in the city center",
                "price": 1200.0,
                "location": "New York, NY",
                "bedrooms": 2,
                "bathrooms": 1,
                "area_sqft": 800.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Cozy Cottage",
                "description": "Charming cottage with garden",
                "price": 900.0,
                "location": "Austin, TX",
                "bedrooms": 1,
                "bathrooms": 1,
                "area_sqft": 600.0,
                "property_type": "cottage",
                "owner_id": user.id
            },
            {
                "title": "Luxury Villa",
                "description": "Spacious luxury villa with pool",
                "price": 5000.0,
                "location": "Los Angeles, CA",
                "bedrooms": 4,
                "bathrooms": 3,
                "area_sqft": 2500.0,
                "property_type": "villa",
                "owner_id": user.id
            },
            {
                "title": "City Studio",
                "description": "Compact studio apartment",
                "price": 700.0,
                "location": "San Francisco, CA",
                "bedrooms": 1,
                "bathrooms": 1,
                "area_sqft": 400.0,
                "property_type": "apartment",
                "owner_id": user.id
            },
            {
                "title": "Suburban House",
                "description": "Family house in quiet neighborhood",
                "price": 1800.0,
                "location": "Seattle, WA",
                "bedrooms": 3,
                "bathrooms": 2,
                "area_sqft": 1800.0,
                "property_type": "villa",
                "owner_id": user.id
            }
        ]

        for house_data in houses_data:
            house = House(**house_data)
            db.add(house)

        db.commit()
    finally:
        db.close()
