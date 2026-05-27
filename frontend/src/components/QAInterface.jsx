import React from 'react';

export default function QAInterface({ documentId }) {
  const [question, setQuestion] = React.useState('');
  const [answer, setAnswer] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/documents/${documentId}/qa`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      const data = await response.json();
      setAnswer(data);
    } catch (error) {
      setAnswer({ answer: 'Error fetching answer' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && askQuestion()}
          className="input flex-1"
          placeholder="Type your question..."
        />
        <button onClick={askQuestion} disabled={loading} className="btn btn-primary">
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>
      {answer && (
        <div className="card p-4">
          <p className="text-gray-800">{answer.answer}</p>
          {answer.sources?.length > 0 && (
            <div className="mt-4 pt-4 border-t">
              <p className="text-sm text-gray-500">Sources: {answer.sources.join(', ')}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
