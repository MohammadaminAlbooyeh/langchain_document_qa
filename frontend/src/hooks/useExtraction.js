import { useState } from 'react';
import api from '../services/api';

export function useExtraction() {
  const [loading, setLoading] = useState(false);
  const [entities, setEntities] = useState(null);

  const extract = async (documentId) => {
    setLoading(true);
    try {
      const res = await api.post(`/documents/${documentId}/extract-entities`);
      setEntities(res.data.entities);
      return res.data.entities;
    } finally {
      setLoading(false);
    }
  };

  return { extract, entities, loading };
}
