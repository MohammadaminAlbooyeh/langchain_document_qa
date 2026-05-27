import { useState } from 'react';
import { askQuestion } from '../services/qa_api';

export function useQA() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const ask = async (documentId, question) => {
    setLoading(true);
    setError(null);
    try {
      const result = await askQuestion(documentId, question);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { ask, loading, error };
}
