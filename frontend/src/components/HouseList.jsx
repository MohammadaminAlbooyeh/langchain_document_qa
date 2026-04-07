import React from "react";

const houses = [
  {
    id: 1,
    title: "Modern Apartment in City Center",
    price: "$1,200/month",
    location: "Downtown",
    description: "A beautiful modern apartment close to all amenities.",
  },
  {
    id: 2,
    title: "Cozy Suburban Home",
    price: "$2,000/month",
    location: "Suburbs",
    description: "Spacious home with a large backyard, perfect for families.",
  },
];

export default function HouseList() {
  return (
    <div style={{ maxWidth: 600, margin: "2rem auto" }}>
      <h2>Available Houses</h2>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {houses.map((house) => (
          <li
            key={house.id}
            style={{
              border: "1px solid #e5e4e7",
              borderRadius: 8,
              padding: 16,
              marginBottom: 16,
              background: "#fff",
              boxShadow: "0 2px 8px rgba(0,0,0,0.04)",
            }}
          >
            <h3 style={{ margin: 0 }}>{house.title}</h3>
            <p style={{ margin: "8px 0 4px 0", color: "#6b6375" }}>{house.location} &mdash; {house.price}</p>
            <p style={{ margin: 0 }}>{house.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
