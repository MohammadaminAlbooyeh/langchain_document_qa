import { ASK_QUESTION, FETCH_HISTORY } from '../actions/qaActions';

const initialState = {
  current: null,
  history: [],
};

export default function qaReducer(state = initialState, action) {
  switch (action.type) {
    case ASK_QUESTION:
      return { ...state, current: action.payload };
    case FETCH_HISTORY:
      return { ...state, history: action.payload };
    default:
      return state;
  }
}
