import React from 'react';

export default function DocumentPreview({ documentId }) {
  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold mb-2">Document Preview</h3>
      <p className="text-gray-500">Preview will appear here after upload.</p>
    </div>
  );
}
