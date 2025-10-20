import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const uploadETFFile = async (file, topHoldingsCount = null) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_BASE_URL}/api/etf/upload`, formData, {
        headers: {'Content-Type': 'multipart/form-data'}
    });

    return response.data;
};
