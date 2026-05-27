import api from '../../services/api';

export const FETCH_DOCUMENTS = 'FETCH_DOCUMENTS';
export const UPLOAD_DOCUMENT = 'UPLOAD_DOCUMENT';
export const DELETE_DOCUMENT = 'DELETE_DOCUMENT';

export const fetchDocuments = () => async (dispatch) => {
  const response = await api.get('/documents');
  dispatch({ type: FETCH_DOCUMENTS, payload: response.data });
};

export const uploadDocument = (file) => async (dispatch) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/documents/upload', formData);
  dispatch({ type: UPLOAD_DOCUMENT, payload: response.data });
  return response.data;
};

export const deleteDocument = (id) => async (dispatch) => {
  await api.delete(`/documents/${id}`);
  dispatch({ type: DELETE_DOCUMENT, payload: id });
};
