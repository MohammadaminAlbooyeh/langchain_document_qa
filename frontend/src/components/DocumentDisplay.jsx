import React from 'react';
import LoadingSpinner from './LoadingSpinner';

export default function DocumentDisplay({ documentId }) {
  const [loading, setLoading] = React.useState(true);
  const [document, setDocument] = React.useState(null);

  React.useEffect(() => {
    const fetchDocument = async () => {
      try {
        const response = await fetch(`/api/v1/documents/${documentId}`);
        const data = await response.json();
        setDocument(data);
      } catch (error) {
        console.error('Failed to fetch document:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDocument();
  }, [documentId]);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold mb-4">{document?.filename}</h2>
      <div className="prose max-w-none">
        <p className="text-gray-600 whitespace-pre-wrap">{document?.text_content?.slice(0, 5000)}</p>
      </div>
    </div>
  );
}
