import React from 'react';
import {useSelector} from 'react-redux';
import Plot from 'react-plotly.js';
import './ETFPrices.css';

const ETFPrices = () => {
    const {etfPrices, loading} = useSelector((state) => state.etf);

    if (loading || !etfPrices || etfPrices.length === 0) {
        return null;
    }

    // Format data for Plotly
    const dates = etfPrices.map(item => item.date);
    const prices = etfPrices.map(item => parseFloat(item.price.toFixed(2)));

    // Calculate statistics
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    const latestPrice = prices[prices.length - 1];

    return (
        <div className="etf-prices-container">
            <div className="chart-header">
                <div>
                    <h2>ETF Price History</h2>
                </div>
            </div>
            <div className="etf-prices-section">
                <div className="chart-wrapper">
                    <Plot
                        data={[
                            {
                                x: dates,
                                y: prices,
                                type: 'scatter',
                                mode: 'lines',
                                line: {
                                    color: '#9C27B0',
                                    width: 2
                                },
                                name: 'ETF Price',
                                hovertemplate: '<b>Date:</b> %{x}<br>' +
                                    '<b>Price:</b> $%{y:.2f}<br>' +
                                    '<extra></extra>'
                            }
                        ]}
                        layout={{
                            autosize: true,
                            title: '',
                            xaxis: {
                                title: 'Date',
                                showgrid: true,
                                gridcolor: '#e0e0e0',
                                zeroline: false,
                                rangeslider: {
                                    visible: true,
                                    thickness: 0.08,
                                    bgcolor: '#f5f5f5',
                                    bordercolor: '#9C27B0',
                                    borderwidth: 1
                                },
                                rangeselector: {
                                    buttons: [
                                        {
                                            count: 7,
                                            label: '1w',
                                            step: 'day',
                                            stepmode: 'backward'
                                        },
                                        {
                                            count: 1,
                                            label: '1m',
                                            step: 'month',
                                            stepmode: 'backward'
                                        },
                                        {
                                            count: 3,
                                            label: '3m',
                                            step: 'month',
                                            stepmode: 'backward'
                                        },
                                        {
                                            count: 6,
                                            label: '6m',
                                            step: 'month',
                                            stepmode: 'backward'
                                        },
                                        {
                                            count: 1,
                                            label: '1y',
                                            step: 'year',
                                            stepmode: 'backward'
                                        },
                                        {
                                            step: 'all',
                                            label: 'All'
                                        }
                                    ],
                                    bgcolor: '#9C27B0',
                                    activecolor: '#7B1FA2',
                                    font: {color: 'white'},
                                    x: 0,
                                    y: 1.05,
                                    xanchor: 'left',
                                    yanchor: 'bottom'
                                }
                            },
                            yaxis: {
                                title: 'Price ($)',
                                showgrid: true,
                                gridcolor: '#e0e0e0',
                                zeroline: false,
                                fixedrange: false
                            },
                            hovermode: 'closest',
                            margin: {
                                l: 60,
                                r: 30,
                                t: 50,
                                b: 100
                            },
                            paper_bgcolor: '#fafafa',
                            plot_bgcolor: '#ffffff',
                            font: {
                                family: 'Arial, sans-serif',
                                size: 12,
                                color: '#333'
                            }
                        }}
                        config={{
                            displayModeBar: false,
                            displaylogo: false,
                            modeBarButtonsToRemove: ['lasso2d', 'select2d'],
                            responsive: true,
                            toImageButtonOptions: {
                                format: 'png',
                                filename: 'etf_price_chart',
                                height: 600,
                                width: 1200,
                                scale: 1
                            }
                        }}
                        style={{width: '100%', height: '600px'}}
                        useResizeHandler={true}
                    />
                </div>

                <div className="price-stats">
                    <div className="stat-item">
                        <span className="stat-label">Data Points:</span>
                        <span className="stat-value">{etfPrices.length} days</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Latest Price:</span>
                        <span className="stat-value">${latestPrice.toFixed(2)}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Price Range:</span>
                        <span className="stat-value">
                            ${minPrice.toFixed(2)} - ${maxPrice.toFixed(2)}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ETFPrices;
