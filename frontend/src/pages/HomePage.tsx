import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">House Finder Bot</h1>
          <nav>
            <ul className="flex space-x-4">
              <li><a href="#" className="text-gray-700 hover:text-blue-600">Home</a></li>
              <li><a href="#" className="text-gray-700 hover:text-blue-600">Search</a></li>
              <li><a href="#" className="text-gray-700 hover:text-blue-600">Favorites</a></li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl font-bold mb-4">Find Your Dream House</h2>
          <p className="mb-6">Search from thousands of houses available for rent or purchase.</p>
          <div className="flex justify-center">
            <input
              type="text"
              placeholder="Enter location..."
              className="px-4 py-2 rounded-l-md border-none focus:outline-none"
            />
            <button className="bg-white text-blue-600 px-4 py-2 rounded-r-md font-bold">Search</button>
          </div>
        </div>
      </section>

      {/* Featured Houses */}
      <section className="py-10">
        <div className="container mx-auto px-4">
          <h3 className="text-2xl font-bold mb-6">Featured Houses</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Example House Cards */}
            <div className="bg-white shadow rounded-lg p-4">
              <img src="https://via.placeholder.com/300" alt="House" className="rounded-md mb-4" />
              <h4 className="text-lg font-bold">Modern Apartment</h4>
              <p className="text-gray-600">$1,200 / month</p>
              <p className="text-gray-600">New York, NY</p>
            </div>
            <div className="bg-white shadow rounded-lg p-4">
              <img src="https://via.placeholder.com/300" alt="House" className="rounded-md mb-4" />
              <h4 className="text-lg font-bold">Cozy Cottage</h4>
              <p className="text-gray-600">$900 / month</p>
              <p className="text-gray-600">Austin, TX</p>
            </div>
            <div className="bg-white shadow rounded-lg p-4">
              <img src="https://via.placeholder.com/300" alt="House" className="rounded-md mb-4" />
              <h4 className="text-lg font-bold">Luxury Villa</h4>
              <p className="text-gray-600">$5,000 / month</p>
              <p className="text-gray-600">Los Angeles, CA</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;