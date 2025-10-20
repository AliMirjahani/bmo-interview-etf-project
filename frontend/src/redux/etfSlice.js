import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import {uploadETFFile} from '../services/api';

export const uploadETF = createAsyncThunk(
    'etf/upload',
    async ({file, topHoldingsCount}, {rejectWithValue}) => {
        try {
            return await uploadETFFile(file, topHoldingsCount);
        } catch (error) {
            return rejectWithValue(error.response?.data || {message: error.message});
        }
    }
);

const etfSlice = createSlice({
    name: 'etf',
    initialState: {
        loading: false,
        error: null,
        constituents: null,
        topHoldings: null,
        etfPrices: null,
        uploadSuccess: false,
    },
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
        clearData: (state) => {
            state.constituents = null;
            state.topHoldings = null;
            state.etfPrices = null;
            state.uploadSuccess = false;
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(uploadETF.pending, (state) => {
                state.loading = true;
                state.error = null;
                state.constituents = null;
                state.topHoldings = null;
                state.etfPrices = null;
                state.uploadSuccess = false;
            })
            .addCase(uploadETF.fulfilled, (state, action) => {
                state.loading = false;
                state.constituents = action.payload.constituents;
                state.etfPrices = action.payload.etf_prices;
                state.topHoldings = action.payload.top_holdings;
                state.uploadSuccess = true;
                state.error = null;
            })
            .addCase(uploadETF.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
                state.uploadSuccess = false;
            });
    },
});

export const {clearError, clearData} = etfSlice.actions;
export default etfSlice.reducer;
