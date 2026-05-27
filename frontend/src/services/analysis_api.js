import api from './api';

export const summarizeDocument = async (documentId, mode = 'paragraphs') => {
  const response = await api.post(`/documents/${documentId}/summarize`, { mode });
  return response.data;
};

export const extractEntities = async (documentId) => {
  const response = await api.post(`/documents/${documentId}/extract-entities`);
  return response.data;
};

export const translateDocument = async (documentId, targetLanguage) => {
  const response = await api.post(`/documents/${documentId}/translate`, {
    target_language: targetLanguage,
  });
  return response.data;
};
