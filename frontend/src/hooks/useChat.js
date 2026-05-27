import { useState, useCallback } from 'react';

export function useChat(documentId) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const send = useCallback(async (message) => {
    setMessages(prev => [...prev, { role: 'user', content: message }]);
    setLoading(true);
    try {
      const res = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_id: documentId, message }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error' }]);
    } finally {
      setLoading(false);
    }
  }, [documentId]);

  return { messages, send, loading };
}
