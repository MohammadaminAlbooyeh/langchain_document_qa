import React, { useState, useEffect } from 'react';

export default function SettingsPage() {
  const [apiUrl, setApiUrl] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setApiUrl(localStorage.getItem('api_url') || 'http://localhost:8000');
    setApiKey(localStorage.getItem('api_key') || '');
  }, []);

  const handleSave = () => {
    localStorage.setItem('api_url', apiUrl);
    localStorage.setItem('api_key', apiKey);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Settings</h1>
      <div className="space-y-4">
        <div className="card p-4">
          <label className="block text-sm font-medium mb-1">API URL</label>
          <input
            type="text"
            className="input w-full"
            value={apiUrl}
            onChange={e => setApiUrl(e.target.value)}
            placeholder="http://localhost:8000"
          />
        </div>
        <div className="card p-4">
          <label className="block text-sm font-medium mb-1">API Key</label>
          <input
            type="password"
            className="input w-full"
            value={apiKey}
            onChange={e => setApiKey(e.target.value)}
            placeholder="Enter API key"
          />
        </div>
        <button onClick={handleSave} className="btn btn-primary">
          {saved ? 'Saved!' : 'Save Settings'}
        </button>
      </div>
    </div>
  );
}
