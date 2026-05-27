import React, { useState, useEffect, useRef } from 'react';
import { askQuestion } from '../services/qa_api';
import LoadingSpinner from './LoadingSpinner';
import toast from 'react-hot-toast';

export default function ChatBox({ documentId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await askQuestion(documentId, userMessage, conversationId);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.answer,
          sources: response.sources,
        },
      ]);
      setConversationId(response.conversation_id);
      toast.success('Response received');
    } catch (error) {
      const errorMsg = error.message || 'Failed to get response';
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Error: ${errorMsg}`,
          isError: true,
        },
      ]);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="card flex flex-col h-[600px] border rounded-lg overflow-hidden">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p>Start a conversation by asking a question...</p>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] p-3 rounded-lg ${
                  msg.role === 'user'
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : msg.isError
                    ? 'bg-red-100 text-red-800 rounded-bl-none'
                    : 'bg-white border border-gray-200 rounded-bl-none'
                }`}
              >
                <p className="text-sm">{msg.content}</p>
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-300 text-xs">
                    <p className="font-semibold mb-1">Sources:</p>
                    {msg.sources.map((src, idx) => (
                      <p key={idx} className="text-gray-600">
                        • {src}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 p-3 rounded-lg rounded-bl-none">
              <LoadingSpinner small />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t bg-white p-4 flex gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          className="input flex-1 resize-none"
          placeholder="Ask a question... (Shift+Enter for new line)"
          rows={2}
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          className="btn btn-primary h-auto self-end"
        >
          {loading ? <LoadingSpinner small /> : 'Send'}
        </button>
      </div>
    </div>
  );
}
