import React from 'react';
import {useSelector} from 'react-redux';
import Plot from 'react-plotly.js';
import './TopHoldings.css';

const TopHoldings = () => {
    const {topHoldings, loading} = useSelector((state) => state.etf);

    if (loading || !topHoldings || topHoldings.length === 0) {
        return null;
    }

    // Format data for Plotly - reverse order so #1 is at the top
    const symbols = topHoldings.map(item => item.name).reverse();
    const holdingSizes = topHoldings.map(item => parseFloat(item.holding_size.toFixed(3))).reverse();

    return (
        <div className="top-holdings-container">
            <h2>Top Holdings ({topHoldings.length})</h2>
            <p className="chart-description">
                Largest holdings ranked by holding size
            </p>
            <div className="top-holdings-section">
                <div className="chart-wrapper">
                    <Plot
                        data={[
                            {
                                x: symbols,
                                y: holdingSizes,
                                type: 'bar',
                                orientation: 'v',
                                marker: {
                                    color: '#FF9800',
                                    opacity: 0.8
                                },
                                hovertemplate: '<b>%{x}</b><br>' +
                                    'Holding Size: %{y:.3f}<br>' +
                                    '<extra></extra>'
                            }
                        ]}
                        layout={{
                            autosize: true,
                            title: '',
                            xaxis: {
                                title: '',
                                showgrid: false,
                                automargin: true,
                            },
                            yaxis: {
                                title: 'Holding Size',
                                showgrid: true,
                                gridcolor: '#e0e0e0',
                                zeroline: true,
                            },
                            hovermode: 'closest',
                            margin: {
                                l: 100,
                                r: 80,
                                t: 30,
                                b: 60
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
                            responsive: true,
                        }}
                        style={{width: '100%', height: '500px'}}
                        useResizeHandler={true}
                    />
                </div>
            </div>
        </div>
    );
};

export default TopHoldings;
