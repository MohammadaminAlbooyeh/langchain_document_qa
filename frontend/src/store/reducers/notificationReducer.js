import { ADD_NOTIFICATION, REMOVE_NOTIFICATION } from '../actions/notificationActions';

const initialState = {
  items: [],
};

export default function notificationReducer(state = initialState, action) {
  switch (action.type) {
    case ADD_NOTIFICATION:
      return { ...state, items: [...state.items, action.payload] };
    case REMOVE_NOTIFICATION:
      return { ...state, items: state.items.filter(n => n.id !== action.payload) };
    default:
      return state;
  }
}
