import { useState } from 'react';

export function useSummarization() {
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState(null);

  const summarize = async (documentId, mode = 'paragraphs') => {
    setLoading(true);
    try {
      const res = await fetch(`/api/v1/documents/${documentId}/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode }),
      });
      const data = await res.json();
      setSummary(data.summary);
      return data.summary;
    } finally {
      setLoading(false);
    }
  };

  return { summarize, summary, loading };
}
