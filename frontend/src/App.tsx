import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import AppRouter from './router/AppRouter';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-blue-600">Welcome to House Finder</h1>
          <p className="text-gray-700 mt-4">Find your dream house with ease!</p>
        </header>
      </div>
      <AppRouter />
    </BrowserRouter>
  );
};

export default App;