import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from 'react-router-dom';
import WidgetPropers from "./components/WidgetPropers";

const anchor = document.getElementById('missalemeum')
const root = ReactDOM.createRoot(anchor);
root.render(
      <BrowserRouter>
        {
          anchor.dataset.widget === undefined
          ? <App {...anchor.dataset} />
          : <WidgetPropers {...anchor.dataset} />
        }
      </BrowserRouter>
);
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
if ('serviceWorker' in navigator && anchor.dataset.widget === undefined) {
    navigator.serviceWorker.register('/service-worker.js');
}
