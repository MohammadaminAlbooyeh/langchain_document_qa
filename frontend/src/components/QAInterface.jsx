import React, { useState, useCallback } from 'react';
import { askQuestion, listConversations } from '../services/qa_api';
import toast from 'react-hot-toast';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

export default function QAInterface({ documentId }) {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [history, setHistory] = useState([]);

  const handleAskQuestion = useCallback(async () => {
    if (!question.trim()) {
      toast.error('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await askQuestion(documentId, question, conversationId);
      setAnswer(response);
      setConversationId(response.conversation_id);
      setHistory([...history, { question, answer: response.answer }]);
      setQuestion('');
      toast.success('Question answered successfully');
    } catch (err) {
      const errorMsg = err.message || 'Failed to get answer';
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  }, [question, documentId, conversationId, history]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAskQuestion();
    }
  };

  return (
    <div className="space-y-4">
      {error && <ErrorMessage message={error} />}
      
      <div className="flex gap-2">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          className="input flex-1 resize-none"
          placeholder="Type your question... (Shift+Enter for new line)"
          rows={3}
          disabled={loading}
        />
        <button
          onClick={handleAskQuestion}
          disabled={loading || !question.trim()}
          className="btn btn-primary h-auto"
        >
          {loading ? <LoadingSpinner small /> : 'Ask'}
        </button>
      </div>

      {answer && (
        <div className="card p-4 space-y-3">
          <div>
            <p className="font-semibold text-gray-900 mb-2">Answer:</p>
            <p className="text-gray-800">{answer.answer}</p>
          </div>
          {answer.sources && answer.sources.length > 0 && (
            <div className="pt-4 border-t">
              <p className="text-sm font-semibold text-gray-600 mb-2">Sources:</p>
              <ul className="text-sm text-gray-500 space-y-1">
                {answer.sources.map((source, idx) => (
                  <li key={idx}>• {source}</li>
                ))}
              </ul>
            </div>
          )}
          {answer.confidence && (
            <div className="pt-2 text-xs text-gray-500">
              Confidence: {(answer.confidence * 100).toFixed(0)}%
            </div>
          )}
        </div>
      )}

      {history.length > 0 && (
        <div className="card p-4">
          <h4 className="font-semibold text-gray-900 mb-3">Conversation History</h4>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {history.map((item, idx) => (
              <div key={idx} className="pb-3 border-b last:border-b-0">
                <p className="text-sm font-semibold text-blue-600">Q: {item.question}</p>
                <p className="text-sm text-gray-700 mt-1">A: {item.answer.substring(0, 150)}...</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
