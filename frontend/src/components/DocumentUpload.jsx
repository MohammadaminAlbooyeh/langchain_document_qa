import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import { uploadDocument } from '../services/document_api';
import toast from 'react-hot-toast';

export default function DocumentUpload() {
  const navigate = useNavigate();

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    try {
      const result = await uploadDocument(file);
      toast.success('Document uploaded successfully');
      navigate(`/analysis/${result.id}`);
    } catch (error) {
      toast.error('Failed to upload document');
    }
  }, [navigate]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'], 'text/plain': ['.txt'] },
    maxFiles: 1,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
        isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
      }`}
    >
      <input {...getInputProps()} />
      <p className="text-lg text-gray-600">
        {isDragActive ? 'Drop your file here' : 'Drag & drop a file, or click to select'}
      </p>
      <p className="text-sm text-gray-400 mt-2">PDF, DOCX, or TXT files</p>
    </div>
  );
}
