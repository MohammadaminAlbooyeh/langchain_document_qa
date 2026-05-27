import React, { useEffect, useState } from 'react';
import { listConversations, getConversation } from '../services/qa_api';
import { deleteDocument } from '../services/document_api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import toast from 'react-hot-toast';

export default function HistoryPage() {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedConv, setSelectedConv] = useState(null);
  const [selectedConvDetails, setSelectedConvDetails] = useState(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await listConversations();
      setConversations(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch conversations');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectConversation = async (convId) => {
    try {
      const details = await getConversation(convId);
      setSelectedConv(convId);
      setSelectedConvDetails(details);
    } catch (err) {
      toast.error('Failed to load conversation details');
    }
  };

  const handleDeleteDocument = async (docId) => {
    if (!window.confirm('Are you sure you want to delete this document?')) return;
    try {
      await deleteDocument(docId);
      await fetchConversations();
      setSelectedConv(null);
      setSelectedConvDetails(null);
      toast.success('Document deleted successfully');
    } catch (err) {
      toast.error('Failed to delete document');
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Conversation History</h1>

      {conversations.length === 0 ? (
        <div className="card p-12 text-center text-gray-500">
          <p>No conversations yet. Start by uploading a document!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Conversations List */}
          <div className="lg:col-span-1">
            <div className="card p-4">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Conversations</h2>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {conversations.map((conv) => (
                  <button
                    key={conv.id}
                    onClick={() => handleSelectConversation(conv.id)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      selectedConv === conv.id
                        ? 'bg-blue-100 border border-blue-300'
                        : 'hover:bg-gray-100 border border-gray-200'
                    }`}
                  >
                    <p className="font-medium text-gray-900 truncate">{conv.title}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(conv.created_at).toLocaleDateString()}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Conversation Details */}
          {selectedConvDetails && (
            <div className="lg:col-span-2">
              <div className="card p-6 space-y-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">
                      {selectedConvDetails.title}
                    </h2>
                    <p className="text-sm text-gray-500 mt-1">
                      Started: {new Date(selectedConvDetails.created_at).toLocaleString()}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDeleteDocument(selectedConvDetails.document_id)}
                    className="btn btn-danger text-sm"
                  >
                    Delete
                  </button>
                </div>

                {/* Q&A History */}
                {selectedConvDetails.history && selectedConvDetails.history.length > 0 ? (
                  <div className="bg-gray-50 rounded-lg p-4 space-y-4 max-h-96 overflow-y-auto">
                    {selectedConvDetails.history.map((item, idx) => (
                      <div key={idx} className="pb-4 border-b last:border-b-0">
                        <p className="font-semibold text-blue-600 text-sm">Q: {item.question}</p>
                        <p className="text-gray-800 mt-2 text-sm">{item.answer}</p>
                        <p className="text-xs text-gray-400 mt-2">
                          {new Date(item.created_at).toLocaleString()}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">No Q&A history in this conversation</p>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
