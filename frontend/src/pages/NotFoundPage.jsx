import React from 'react';
import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div className="text-center py-20">
      <h1 className="text-6xl font-bold text-gray-300 mb-4">404</h1>
      <p className="text-xl text-gray-500 mb-6">Page not found</p>
      <Link to="/" className="btn btn-primary">Go Home</Link>
    </div>
  );
}
