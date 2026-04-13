// API service for fetching houses from backend

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8002";

export async function fetchHouses({ mode, price, city, district, rooms }) {
  // Example endpoint: /houses?mode=rent&min_price=200&max_price=1000&city=Rome&rooms=2
  const params = new URLSearchParams();
  params.append("mode", mode);
  params.append("min_price", price[0]);
  params.append("max_price", price[1]);
  if (city) params.append("city", city);
  if (district) params.append("district", district);
  if (rooms) params.append("rooms", rooms);

  const res = await fetch(`${API_BASE}/houses/?${params.toString()}`);
  if (!res.ok) {
    const contentType = res.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      const payload = await res.json().catch(() => null);
      const message = payload?.detail || payload?.message || "Failed to fetch houses";
      throw new Error(message);
    }
    const detail = await res.text();
    throw new Error(detail || "Failed to fetch houses");
  }
  return res.json();
}

// Fetch districts for a given city
export async function fetchDistricts(city) {
  const res = await fetch(`${API_BASE}/houses/districts?city=${encodeURIComponent(city)}`);
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || "Failed to fetch districts");
  }
  return res.json();
}
