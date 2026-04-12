
import { useState } from "react";
import FilterBox from "./components/FilterBox";
import HouseList from "./components/HouseList";
import "./App.css";


function App() {
  const [filters, setFilters] = useState({ mode: "rent", price: [200, 10000] });

  return (
    <div className="app-shell">
      <header className="hero-header">
        <p className="hero-kicker">Smart Search, Better Living</p>
        <h1>House Finder Italy</h1>
        <p className="hero-subtitle">Discover rental and purchase opportunities across Italian cities.</p>
      </header>
      <main className="content-grid">
        <FilterBox onSearch={setFilters} />
        <HouseList filters={filters} />
      </main>
    </div>
  );
}

export default App;
