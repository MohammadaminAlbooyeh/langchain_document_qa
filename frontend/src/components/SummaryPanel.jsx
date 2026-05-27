import React from 'react';

export default function SummaryPanel({ documentId }) {
  const [summary, setSummary] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const generateSummary = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/documents/${documentId}/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: 'paragraphs' }),
      });
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      setSummary('Error generating summary');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold mb-2">Summary</h3>
      {!summary ? (
        <button onClick={generateSummary} disabled={loading} className="btn btn-secondary">
          {loading ? 'Generating...' : 'Generate Summary'}
        </button>
      ) : (
        <p className="text-gray-700">{summary}</p>
      )}
    </div>
  );
}
