import React, { useState, useRef } from "react";
const CITIES = [
  "Rome",
  "Milan",
  "Turin",
  "Naples",
  "Florence",
  "Venice",
  "Bologna",
  "Genoa",
  "Palermo",
  "Bari",
  "Catania",
  "Verona",
  "Messina",
  "Padua",
  "Trieste",
  "Taranto",
  "Brescia",
  "Prato",
  "Parma",
  "Modena",
  "Reggio Calabria"
];
import { fetchDistricts } from "../services/api";

function FilterBox({ onSearch }) {
  const [mode, setMode] = useState("rent");
  const [price, setPrice] = useState([200, 10000]);
  const [city, setCity] = useState("");
  const [district, setDistrict] = useState("");
  const districtSelectRef = useRef(null);
  const [citySuggestions, setCitySuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const cityInputRef = useRef(null);
  const [districts, setDistricts] = useState([]);
  const [rooms, setRooms] = useState(1);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({ mode, price, city, district, rooms });
  };

  // Update price range when mode changes
  const handleModeChange = (e) => {
    const newMode = e.target.value;
    setMode(newMode);
    if (newMode === "rent") {
      setPrice([200, 10000]);
    } else {
      setPrice([20000, 2000000]);
    }
  };

  // Handle price slider change
  const handlePriceChange = (e) => {
    const min = Number(e.target.name === "min" ? e.target.value : price[0]);
    const max = Number(e.target.name === "max" ? e.target.value : price[1]);
    setPrice([min, max]);
  };

  // Handle city change
  const handleCityChange = async (e) => {
    const value = e.target.value;
    setCity(value);
    setDistrict("");
    if (value.length > 0) {
      const filtered = CITIES.filter((c) => c.toLowerCase().startsWith(value.toLowerCase()));
      setCitySuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setCitySuggestions([]);
      setShowSuggestions(false);
    }
    // Districts only update if a valid city is selected
    setDistricts([]);
  };

  const handleCityKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      // If a suggestion matches the current text, select it
      const match = citySuggestions.find(
        (s) => s.toLowerCase() === city.toLowerCase()
      );
      if (match) {
        handleCitySelect(match);
      }
      // Trigger search with current filters
      onSearch({ mode, price, city, district, rooms });
    }
  };

  const handleCitySelect = async (selectedCity) => {
    setCity(selectedCity);
    setShowSuggestions(false);
    setDistrict("");
    try {
      const dists = await fetchDistricts(selectedCity);
      setDistricts(dists);
    } catch {
      setDistricts([]);
    }
    // Move focus away from input
    cityInputRef.current && cityInputRef.current.blur();
    // If districts were loaded, focus the district select so user can pick
    setTimeout(() => {
      if (districtSelectRef.current) districtSelectRef.current.focus();
    }, 50);
  };

  const handleDistrictChange = (e) => {
    setDistrict(e.target.value);
  };

  // Handle rooms change
  const handleRoomsChange = (e) => {
    setRooms(e.target.value);
  };

  return (
    <form className="filter-panel" aria-label="Search Filters" onSubmit={handleSubmit}>
      <div className="mode-switch" role="radiogroup" aria-label="Listing mode">
        <label className={`mode-option ${mode === "rent" ? "is-active" : ""}`}>
          <input
            type="radio"
            value="rent"
            checked={mode === "rent"}
            onChange={handleModeChange}
          />
          <span>Rent</span>
        </label>
        <label className={`mode-option ${mode === "buy" ? "is-active" : ""}`}>
          <input
            type="radio"
            value="buy"
            checked={mode === "buy"}
            onChange={handleModeChange}
          />
          <span>Buy</span>
        </label>
      </div>

      <div className="form-row">
        <label className="field-label">
          Price range ({mode === "rent" ? "€/month" : "€"}):
        </label>
        <div className="range-inputs">
          <input
            type="number"
            name="min"
            min={mode === "rent" ? 200 : 20000}
            max={price[1]}
            value={price[0]}
            onChange={handlePriceChange}
            className="text-input"
          />
          <span className="range-separator">to</span>
          <input
            type="number"
            name="max"
            min={price[0]}
            max={mode === "rent" ? 10000 : 2000000}
            value={price[1]}
            onChange={handlePriceChange}
            className="text-input"
          />
        </div>
      </div>

      <div className="form-row" style={{ position: "relative" }}>
        <label className="field-label">City:</label>
        <input
          type="text"
          value={city}
          onChange={handleCityChange}
          onKeyDown={handleCityKeyDown}
          placeholder="e.g. Rome, Milan"
          className="text-input full-width"
          autoComplete="off"
          ref={cityInputRef}
          onFocus={() => city && setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 120)}
        />
        {showSuggestions && citySuggestions.length > 0 && (
          <ul className="city-suggestions">
            {citySuggestions.map((suggestion) => (
              <li
                key={suggestion}
                className="city-suggestion-item"
                onMouseDown={() => handleCitySelect(suggestion)}
              >
                {suggestion}
              </li>
            ))}
          </ul>
        )}
      </div>

      {districts.length > 0 && (
        <div className="form-row">
          <label className="field-label">District:</label>
          <select ref={districtSelectRef} value={district} onChange={handleDistrictChange} className="text-input full-width">
            <option value="">All districts</option>
            {districts.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
      )}

      <div className="form-row">
        <label className="field-label">Rooms:</label>
        <input
          type="number"
          min={1}
          max={10}
          value={rooms}
          onChange={handleRoomsChange}
          placeholder="e.g. 2"
          className="text-input"
        />
      </div>

      <button type="submit" className="search-button">Search Houses</button>
    </form>
  );
}

export default FilterBox;
