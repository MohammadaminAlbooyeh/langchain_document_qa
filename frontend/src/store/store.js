import { configureStore } from '@reduxjs/toolkit';
import documentReducer from './reducers/documentReducer';
import qaReducer from './reducers/qaReducer';
import chatReducer from './reducers/chatReducer';
import notificationReducer from './reducers/notificationReducer';

export const store = configureStore({
  reducer: {
    documents: documentReducer,
    qa: qaReducer,
    chat: chatReducer,
    notifications: notificationReducer,
  },
});
