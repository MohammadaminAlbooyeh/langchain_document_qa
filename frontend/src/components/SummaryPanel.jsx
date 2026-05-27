import React, { useState, useEffect } from 'react';
import { summarizeDocument } from '../services/analysis_api';
import toast from 'react-hot-toast';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

export default function SummaryPanel({ documentId }) {
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('paragraphs');
  const [generated, setGenerated] = useState(false);

  const generateSummary = async () => {
    setLoading(true);
    setError(null);
    setSummary('');
    try {
      const response = await summarizeDocument(documentId, mode);
      setSummary(response.summary);
      setGenerated(true);
      toast.success('Summary generated successfully');
    } catch (err) {
      const errorMsg = err.message || 'Failed to generate summary';
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-4 space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Document Summary</h3>
      
      {!generated ? (
        <>
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">Summary Mode:</label>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="input w-full"
              disabled={loading}
            >
              <option value="paragraphs">Paragraphs</option>
              <option value="bullet_points">Bullet Points</option>
              <option value="sections">Sections</option>
            </select>
          </div>
          <button
            onClick={generateSummary}
            disabled={loading}
            className="btn btn-secondary w-full"
          >
            {loading ? <LoadingSpinner small /> : 'Generate Summary'}
          </button>
        </>
      ) : (
        <>
          {error && <ErrorMessage message={error} />}
          {summary && (
            <div className="bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
              <p className="text-gray-800 whitespace-pre-wrap">{summary}</p>
            </div>
          )}
          <button
            onClick={() => {
              setSummary('');
              setGenerated(false);
              setError(null);
            }}
            className="btn btn-secondary w-full"
          >
            Generate New Summary
          </button>
        </>
      )}
    </div>
  );
}
