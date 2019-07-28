import React from 'react';
import logo from './logo.svg';
import Login from './Login/Login.js';
import './App.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import AppRouter from './AppRouter/AppRouter.js';

function App() {
  return (
    <div className="App">
      <AppRouter></AppRouter>
    </div>
  );
}

export default App;
