import './App.css';
import Menu from './components/Menu';
import ForcastGraph from './components/ForecastGraph';
import PerformanceGraph from './components/PerformanceGraph';
import {ReactComponent as Stocks} from './assets/stock-increase.svg';

function App() {





    return (
        <div className='app-container'>
            <div className='header'> 
                <h1>Stock Forecast</h1>
                <Stocks />
            </div>

            <div className='main'>
                
            </div>

            <div className='footer'>
                <h1>Alexander Carvalho · 2022 ©</h1>
            </div>
        </div>
    );
}

export default App;
