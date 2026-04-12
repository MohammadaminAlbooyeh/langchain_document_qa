import React, { useEffect, useState } from "react";
import { fetchHouses } from "../services/api";

export default function HouseList({ filters }) {
  const [houses, setHouses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const formatPrice = (value) =>
    new Intl.NumberFormat("en-IT", {
      maximumFractionDigits: 0,
    }).format(value ?? 0);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchHouses(filters)
      .then((data) => {
        setHouses(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to fetch houses");
        setLoading(false);
      });
  }, [filters]);

  return (
    <section className="results-panel" aria-live="polite">
      <div className="results-header">
        <h2>Available Houses</h2>
        <span className="results-count">{houses.length} result{houses.length === 1 ? "" : "s"}</span>
      </div>
      {loading ? (
        <div className="status-message">Loading properties...</div>
      ) : error ? (
        <div className="status-message error">{error}</div>
      ) : (
        <ul className="house-list">
          {houses.length === 0 ? (
            <li className="status-message">No houses found for selected filters.</li>
          ) : (
            houses.map((house) => (
              <li key={house.id} className="house-card">
                <div className="house-card-header">
                  <h3>{house.title}</h3>
                  <span className="price-chip">€ {formatPrice(house.price)}</span>
                </div>
                <p className="location-line">{house.location}</p>
                <p className="description-line">{house.description || "No description available."}</p>
                <div className="house-meta">
                  <span>{house.bedrooms} bd</span>
                  <span>{house.bathrooms} ba</span>
                  <span>{house.area_sqft} sqft</span>
                  <span>{house.property_type}</span>
                </div>
              </li>
            ))
          )}
        </ul>
      )}
    </section>
  );
}
