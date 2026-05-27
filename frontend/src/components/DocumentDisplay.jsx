import React, { useEffect, useState } from 'react';
import { getDocument } from '../services/document_api';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

export default function DocumentDisplay({ documentId }) {
  const [loading, setLoading] = useState(true);
  const [document, setDocument] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getDocument(documentId);
        setDocument(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch document');
      } finally {
        setLoading(false);
      }
    };
    fetchDocument();
  }, [documentId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="card p-6 space-y-4">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">{document?.filename}</h2>
        <div className="flex gap-4 text-sm text-gray-600">
          <span>Type: {document?.file_type?.toUpperCase()}</span>
          <span>Size: {(document?.file_size / 1024).toFixed(2)} KB</span>
          <span className={`font-semibold ${
            document?.status === 'processed' ? 'text-green-600' : 
            document?.status === 'processing' ? 'text-blue-600' :
            document?.status === 'failed' ? 'text-red-600' :
            'text-yellow-600'
          }`}>
            Status: {document?.status}
          </span>
        </div>
      </div>

      {document?.status === 'processing' && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-center gap-3">
          <LoadingSpinner small />
          <span className="text-blue-800">Document is being processed. Please wait...</span>
        </div>
      )}

      {document?.status === 'failed' && (
        <ErrorMessage message="Document processing failed. Please try uploading again." />
      )}

      {document?.status === 'processed' && document?.text_content && (
        <div className="bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
          <p className="text-gray-800 whitespace-pre-wrap text-sm leading-relaxed">
            {document.text_content.slice(0, 5000)}
            {document.text_content.length > 5000 && '...'}
          </p>
        </div>
      )}

      {document?.status !== 'processed' && !document?.text_content && (
        <div className="text-center py-8 text-gray-500">
          <p>Waiting for document processing...</p>
        </div>
      )}
    </div>
  );
}
