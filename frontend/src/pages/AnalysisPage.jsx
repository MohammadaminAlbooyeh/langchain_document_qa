import React from 'react';
import { useParams } from 'react-router-dom';
import DocumentDisplay from '../components/DocumentDisplay';
import SummaryPanel from '../components/SummaryPanel';
import EntityList from '../components/EntityList';

export default function AnalysisPage() {
  const { id } = useParams();

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Document Analysis</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DocumentDisplay documentId={id} />
        <div className="space-y-6">
          <SummaryPanel documentId={id} />
          <EntityList documentId={id} />
        </div>
      </div>
    </div>
  );
}
