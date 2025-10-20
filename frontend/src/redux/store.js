import { configureStore } from '@reduxjs/toolkit';
import etfReducer from './etfSlice';

export const store = configureStore({
  reducer: {
    etf: etfReducer,
  },
});
