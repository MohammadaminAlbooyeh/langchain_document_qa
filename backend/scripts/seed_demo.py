#!/usr/bin/env python3
"""Seed the development database with demo houses."""
from app.db.database import SessionLocal, init_db
from app.models.house import House


def seed():
    init_db()
    db = SessionLocal()
    demos = [
        House(title="Cozy 1-bedroom near center", price=85000, city="Torino", neighborhood="Centro", area_m2=45.0, rooms=2, url="https://example.com/1"),
        House(title="Spacious 3-room apartment", price=165000, city="Torino", neighborhood="San Salvario", area_m2=110.0, rooms=3, url="https://example.com/2"),
        House(title="Studio with balcony", price=65000, city="Torino", neighborhood="Crocetta", area_m2=30.0, rooms=1, url="https://example.com/3"),
        House(title="Renovated loft", price=230000, city="Torino", neighborhood="Vanchiglia", area_m2=150.0, rooms=4, url="https://example.com/4"),
    ]
    db.add_all(demos)
    db.commit()
    count = db.query(House).count()
    db.close()
    print(f"Seeded demo houses. Total houses: {count}")


if __name__ == "__main__":
    seed()
