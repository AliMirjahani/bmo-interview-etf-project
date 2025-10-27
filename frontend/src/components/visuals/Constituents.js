import React, {useMemo, useState} from 'react';
import {useSelector} from 'react-redux';
import {AgGridReact} from 'ag-grid-react';
import {ModuleRegistry, AllCommunityModule} from 'ag-grid-community';
import './Constituents.css';

// Register AG Grid modules
ModuleRegistry.registerModules([AllCommunityModule]);

const Constituents = () => {
    const {constituents, loading} = useSelector((state) => state.etf);
    const [searchText, setSearchText] = useState('');

    const columnDefs = useMemo(() => [
        {
            headerName: 'Symbol',
            field: 'name',
            sortable: true,
            flex: 1,
            cellStyle: {
                fontWeight: '600',
                color: '#2196F3',
                fontFamily: 'monospace'
            }
        },
        {
            headerName: 'Weight',
            field: 'weight',
            sortable: true,
            flex: 1,
            valueFormatter: (params) => {
                if (params.value === undefined || params.value === null) return '';
                return `${(params.value * 100).toFixed(3)}%`;
            },
            comparator: (valueA, valueB) => valueA - valueB
        },
        {
            headerName: 'Price',
            field: 'price',
            sortable: true,
            flex: 1,
            valueFormatter: (params) => {
                if (params.value === undefined || params.value === null) return '';
                return `$${params.value.toFixed(2)}`;
            },
            comparator: (valueA, valueB) => valueA - valueB
        }
    ], []);

    // Default column properties
    const defaultColDef = useMemo(() => ({
        resizable: true,
        sortable: true,
    }), []);

    const filteredData = useMemo(() => {
        if (!constituents) return [];
        if (searchText.trim() === '') return constituents;

        return constituents.filter(item =>
            item.name.toLowerCase().includes(searchText.toLowerCase())
        );
    }, [constituents, searchText]);

    if (loading || !constituents || constituents.length === 0) {
        return null;
    }

    // Calculate dynamic height based on number of rows
    // Support up to 50 items without scrolling
    // Header: ~45px, Row: ~42px, Footer: ~10px
    const rowHeight = 42;
    const headerHeight = 45;
    const footerHeight = 10;
    const maxItems = 50; // Support up to 50 items
    const maxHeight = headerHeight + (maxItems * rowHeight) + footerHeight; // ~2155px
    const minHeight = 150;

    const calculatedHeight = Math.min(
        Math.max(headerHeight + (filteredData.length * rowHeight) + footerHeight, minHeight),
        maxHeight
    );

    return (
        <div className="constituents-container">
            <h2>Constituents ({constituents.length})</h2>

            <div className="search-box-container">
                <input
                    type="text"
                    className="search-input"
                    placeholder="Search by symbol..."
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                />
                {searchText && (
                    <button
                        className="clear-search-btn"
                        onClick={() => setSearchText('')}
                    >
                        ✕
                    </button>
                )}
                <span className="search-results-count">
                    {filteredData.length} of {constituents.length} stocks
                </span>
            </div>

            <div className="constituents-section">
                <div className="ag-theme-alpine" style={{height: `${calculatedHeight}px`, width: '100%'}}>
                    <AgGridReact
                        rowData={filteredData}
                        columnDefs={columnDefs}
                        defaultColDef={defaultColDef}
                        pagination={false}
                        animateRows={true}
                        suppressNoRowsOverlay={false}
                        overlayNoRowsTemplate={'<span>No stocks found</span>'}
                        domLayout='normal'
                        theme= 'themeBalham'
                    />
                </div>
            </div>
        </div>
    );
};

export default Constituents;
