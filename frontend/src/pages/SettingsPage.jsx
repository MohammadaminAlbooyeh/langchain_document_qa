import React from 'react';

export default function SettingsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Settings</h1>
      <div className="space-y-4">
        <div className="card p-4">
          <label className="block text-sm font-medium mb-1">API URL</label>
          <input type="text" className="input" placeholder="http://localhost:8000" />
        </div>
        <div className="card p-4">
          <label className="block text-sm font-medium mb-1">API Key</label>
          <input type="password" className="input" placeholder="Enter API key" />
        </div>
      </div>
    </div>
  );
}
