import React from 'react';
import { useParams } from 'react-router-dom';
import QAInterface from '../components/QAInterface';

export default function QAPage() {
  const { id } = useParams();

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Ask Questions</h1>
      <QAInterface documentId={id} />
    </div>
  );
}
