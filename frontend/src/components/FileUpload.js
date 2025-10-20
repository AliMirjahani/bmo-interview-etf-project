import React, {useState} from 'react';
import {useDispatch, useSelector} from 'react-redux';
import {uploadETF, clearData} from '../redux/etfSlice';
import './FileUpload.css';

const FileUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [validationError, setValidationError] = useState(null);
    const dispatch = useDispatch();
    const {loading, error, uploadSuccess} = useSelector((state) => state.etf);
    console.log(error);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setValidationError(null); // Clear previous validation errors

        if (file) {
            // Validate file type
            if (!file.name.endsWith('.csv')) {
                setValidationError('Please select a CSV file');
                event.target.value = null;
                return;
            }
            setSelectedFile(file);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!selectedFile) {
            setValidationError('Please select a file first');
            return;
        }

        dispatch(uploadETF({file: selectedFile}));
    };

    const handleReset = () => {
        setSelectedFile(null);
        setValidationError(null);
        dispatch(clearData());
        document.getElementById('file-input').value = null;
    };

    return (
        <div className="file-upload-container">
            <h2>ETF File Upload</h2>

            <form onSubmit={handleSubmit} className="upload-form">
                <div className="form-group">
                    <label htmlFor="file-input">Select CSV File:</label>
                    <input
                        id="file-input"
                        type="file"
                        accept=".csv"
                        onChange={handleFileChange}
                        disabled={loading}
                        className="file-input"
                    />
                    {selectedFile && (
                        <p className="file-name">Selected: {selectedFile.name}</p>
                    )}
                </div>

                <div className="button-group">
                    <button type="submit" disabled={loading || !selectedFile} className="btn-primary">
                        {loading ? 'Uploading...' : 'Upload'}
                    </button>
                    <button type="button" onClick={handleReset} disabled={loading} className="btn-secondary">
                        Reset
                    </button>
                </div>
            </form>

            {validationError && (
                <div className="error-message">
                    <h3>Validation Error</h3>
                    <p className="error-text">{validationError}</p>
                </div>
            )}

            {error && (
                <div className="error-message">
                    <h3>Upload Error</h3>
                    <p className="error-text">{error.error || 'An error occurred during upload. Contact system maintainer.'}</p>
                    {error.error_detail && <p className="error-detail">{error.error_detail}</p>}
                </div>
            )}

            {uploadSuccess && (
                <div className="success-message">
                    <p>File uploaded successfully!</p>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
