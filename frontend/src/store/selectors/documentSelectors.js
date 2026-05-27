export const selectDocuments = (state) => state.documents.list;
export const selectCurrentDocument = (state) => state.documents.current;
export const selectDocumentById = (id) => (state) =>
  state.documents.list.find(d => d.id === id);
