import { useState } from 'react';
import { uploadDocument } from '../services/document_api';

export function useDocumentUpload() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const upload = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const data = await uploadDocument(file);
      setResult(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { upload, loading, error, result };
}
