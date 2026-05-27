import React, { useState } from 'react';
import { extractEntities } from '../services/analysis_api';
import toast from 'react-hot-toast';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

export default function EntityList({ documentId }) {
  const [entities, setEntities] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [extracted, setExtracted] = useState(false);

  const handleExtractEntities = async () => {
    setLoading(true);
    setError(null);
    setEntities(null);
    try {
      const response = await extractEntities(documentId);
      setEntities(response.entities);
      setExtracted(true);
      toast.success('Entities extracted successfully');
    } catch (err) {
      const errorMsg = err.message || 'Failed to extract entities';
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-4 space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Named Entities</h3>

      {!extracted ? (
        <button
          onClick={handleExtractEntities}
          disabled={loading}
          className="btn btn-secondary w-full"
        >
          {loading ? <LoadingSpinner small /> : 'Extract Entities'}
        </button>
      ) : (
        <>
          {error && <ErrorMessage message={error} />}
          {entities && Object.keys(entities).length > 0 ? (
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {Object.entries(entities).map(([category, items]) => (
                <div key={category} className="pb-3 border-b last:border-b-0">
                  <h4 className="text-sm font-semibold text-gray-700 uppercase mb-2">
                    {category}
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {items && Array.isArray(items) && items.length > 0 ? (
                      items.map((item, i) => (
                        <span
                          key={i}
                          className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full font-medium"
                        >
                          {item}
                        </span>
                      ))
                    ) : (
                      <span className="text-sm text-gray-500 italic">No entities found</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500 text-center py-4">No entities found in document</p>
          )}
          <button
            onClick={() => {
              setEntities(null);
              setExtracted(false);
              setError(null);
            }}
            className="btn btn-secondary w-full"
          >
            Extract Again
          </button>
        </>
      )}
    </div>
  );
}
