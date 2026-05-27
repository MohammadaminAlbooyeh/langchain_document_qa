import api from './api';

export const askQuestion = async (documentId, question, conversationId) => {
  const response = await api.post(`/documents/${documentId}/qa`, {
    question,
    conversation_id: conversationId,
  });
  return response.data;
};

export const getConversation = async (conversationId) => {
  const response = await api.get(`/conversations/${conversationId}`);
  return response.data;
};

export const listConversations = async () => {
  const response = await api.get('/conversations');
  return response.data;
};
