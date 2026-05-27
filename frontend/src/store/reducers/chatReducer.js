import { SEND_MESSAGE } from '../actions/chatActions';

const initialState = {
  messages: [],
};

export default function chatReducer(state = initialState, action) {
  switch (action.type) {
    case SEND_MESSAGE:
      return { ...state, messages: [...state.messages, action.payload] };
    default:
      return state;
  }
}
