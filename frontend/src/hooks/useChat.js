import { useState, useCallback } from 'react';
import api from '../services/api';

export function useChat(documentId) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const send = useCallback(async (message) => {
    setMessages(prev => [...prev, { role: 'user', content: message }]);
    setLoading(true);
    try {
      const res = await api.post(`/conversations/${documentId}/chat`, {
        question: message,
      });
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.answer }]);
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error' }]);
    } finally {
      setLoading(false);
    }
  }, [documentId]);

  return { messages, send, loading };
}
