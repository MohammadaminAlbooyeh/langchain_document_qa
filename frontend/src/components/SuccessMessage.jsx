import React from 'react';

export default function SuccessMessage({ message }) {
  return (
    <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
      {message || 'Success'}
    </div>
  );
}
