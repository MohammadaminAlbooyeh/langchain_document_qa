import React from 'react';
import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">LangChain Document QA</h1>
      <p className="text-gray-600 mb-8">Upload documents and ask questions using AI-powered analysis.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/upload" className="card p-6 hover:shadow-lg transition-shadow">
          <h3 className="text-xl font-semibold mb-2">Upload Document</h3>
          <p className="text-gray-500">Upload PDF, DOCX, or TXT files for analysis.</p>
        </Link>
        <Link to="/history" className="card p-6 hover:shadow-lg transition-shadow">
          <h3 className="text-xl font-semibold mb-2">View History</h3>
          <p className="text-gray-500">Browse past conversations and analyses.</p>
        </Link>
        <Link to="/settings" className="card p-6 hover:shadow-lg transition-shadow">
          <h3 className="text-xl font-semibold mb-2">Settings</h3>
          <p className="text-gray-500">Configure API keys and preferences.</p>
        </Link>
      </div>
    </div>
  );
}
