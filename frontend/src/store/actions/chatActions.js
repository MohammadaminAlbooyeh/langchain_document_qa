export const SEND_MESSAGE = 'SEND_MESSAGE';
export const SEND_MESSAGE_SUCCESS = 'SEND_MESSAGE_SUCCESS';
export const SEND_MESSAGE_FAILURE = 'SEND_MESSAGE_FAILURE';

export const sendMessage = (message) => ({
  type: SEND_MESSAGE,
  payload: message,
});

export const sendMessageSuccess = (response) => ({
  type: SEND_MESSAGE_SUCCESS,
  payload: response,
});

export const sendMessageFailure = (error) => ({
  type: SEND_MESSAGE_FAILURE,
  payload: error,
});
