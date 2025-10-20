import './App.css';
import FileUpload from './components/FileUpload';
import Constituents from './components/visuals/Constituents';
import TopHoldings from './components/visuals/TopHoldings';
import ETFPrices from './components/visuals/ETFPrices';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>ETF Price Monitor</h1>
            </header>
            <main>
                <FileUpload/>
                <Constituents/>
                <TopHoldings/>
                <ETFPrices/>
            </main>
        </div>
    );
}

export default App;
