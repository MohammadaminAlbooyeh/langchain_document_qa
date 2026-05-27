import React from 'react';

export default function EntityList({ documentId }) {
  const [entities, setEntities] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const extractEntities = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/documents/${documentId}/extract-entities`, {
        method: 'POST',
      });
      const data = await response.json();
      setEntities(data.entities);
    } catch (error) {
      console.error('Extraction failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!entities) {
    return (
      <div className="card p-4">
        <h3 className="text-lg font-semibold mb-2">Entities</h3>
        <button onClick={extractEntities} disabled={loading} className="btn btn-secondary">
          {loading ? 'Extracting...' : 'Extract Entities'}
        </button>
      </div>
    );
  }

  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold mb-2">Extracted Entities</h3>
      {Object.entries(entities).map(([category, items]) => (
        <div key={category} className="mb-3">
          <h4 className="text-sm font-medium text-gray-500 uppercase">{category}</h4>
          <div className="flex flex-wrap gap-1 mt-1">
            {items.map((item, i) => (
              <span key={i} className="px-2 py-1 bg-blue-50 text-blue-700 text-sm rounded">{item}</span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
