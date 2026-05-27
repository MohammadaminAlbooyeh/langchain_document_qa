import api from '../../services/api';

export const ASK_QUESTION = 'ASK_QUESTION';
export const FETCH_HISTORY = 'FETCH_HISTORY';

export const askQuestion = (documentId, question) => async (dispatch) => {
  const response = await api.post(`/documents/${documentId}/qa`, { question });
  dispatch({ type: ASK_QUESTION, payload: response.data });
  return response.data;
};

export const fetchHistory = (conversationId) => async (dispatch) => {
  const response = await api.get(`/conversations/${conversationId}`);
  dispatch({ type: FETCH_HISTORY, payload: response.data });
};
