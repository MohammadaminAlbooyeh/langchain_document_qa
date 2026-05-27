import { useState } from 'react';

export function useExtraction() {
  const [loading, setLoading] = useState(false);
  const [entities, setEntities] = useState(null);

  const extract = async (documentId) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/documents/${documentId}/extract-entities`, {
        method: 'POST',
      });
      const data = await res.json();
      setEntities(data.entities);
      return data.entities;
    } finally {
      setLoading(false);
    }
  };

  return { extract, entities, loading };
}
