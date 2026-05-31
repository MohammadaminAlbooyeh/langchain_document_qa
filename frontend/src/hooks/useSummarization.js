import { useState } from 'react';
import api from '../services/api';

export function useSummarization() {
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState(null);

  const summarize = async (documentId, mode = 'paragraphs') => {
    setLoading(true);
    try {
      const res = await api.post(`/documents/${documentId}/summarize`, { mode });
      setSummary(res.data.summary);
      return res.data.summary;
    } finally {
      setLoading(false);
    }
  };

  return { summarize, summary, loading };
}
