import React from 'react';
import { Link } from 'react-router-dom';

export default function Header({ onToggleSidebar }) {
  return (
    <header className="bg-white border-b px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <button onClick={onToggleSidebar} className="p-1 hover:bg-gray-100 rounded">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 12h18M3 6h18M3 18h18" />
          </svg>
        </button>
        <Link to="/" className="text-xl font-bold text-blue-600">DocQA</Link>
      </div>
      <nav className="flex items-center gap-4">
        <Link to="/upload" className="text-sm text-gray-600 hover:text-blue-600">Upload</Link>
        <Link to="/history" className="text-sm text-gray-600 hover:text-blue-600">History</Link>
      </nav>
    </header>
  );
}
