import React, { useState, useEffect } from 'react';
import { getDocument } from '../services/document_api';

export default function DocumentPreview({ documentId }) {
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!documentId) return;
    setLoading(true);
    getDocument(documentId)
      .then(setDoc)
      .finally(() => setLoading(false));
  }, [documentId]);

  if (!documentId) {
    return (
      <div className="card p-4">
        <h3 className="text-lg font-semibold mb-2">Document Preview</h3>
        <p className="text-gray-500">Preview will appear here after upload.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="card p-4">
        <h3 className="text-lg font-semibold mb-2">Document Preview</h3>
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold mb-2">Document Preview</h3>
      {doc ? (
        <div className="space-y-2">
          <p><span className="font-medium">Filename:</span> {doc.filename}</p>
          <p><span className="font-medium">Type:</span> {doc.file_type}</p>
          <p><span className="font-medium">Size:</span> {(doc.file_size / 1024).toFixed(1)} KB</p>
          <p><span className="font-medium">Status:</span> {doc.status}</p>
        </div>
      ) : (
        <p className="text-gray-500">Document not found.</p>
      )}
    </div>
  );
}
