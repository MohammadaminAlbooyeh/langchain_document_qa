import { FETCH_DOCUMENTS, UPLOAD_DOCUMENT, DELETE_DOCUMENT } from '../actions/documentActions';

const initialState = {
  list: [],
  current: null,
};

export default function documentReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_DOCUMENTS:
      return { ...state, list: action.payload };
    case UPLOAD_DOCUMENT:
      return { ...state, list: [action.payload, ...state.list], current: action.payload };
    case DELETE_DOCUMENT:
      return { ...state, list: state.list.filter(d => d.id !== action.payload) };
    default:
      return state;
  }
}
