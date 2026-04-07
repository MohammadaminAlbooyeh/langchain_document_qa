import HouseList from "./components/HouseList";

function App() {
  return (
    <div>
      <header style={{ padding: "1.5rem 0", textAlign: "center" }}>
        <h1>House Finder Italy</h1>
        <p style={{ color: "#6b6375" }}>Find your next home easily</p>
      </header>
      <main>
        <HouseList />
      </main>
    </div>
  );
}

export default App;
