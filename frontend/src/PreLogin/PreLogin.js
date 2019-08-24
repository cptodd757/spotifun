import React, { Component } from 'react';
import './PreLogin.css';
import logo from '../logo.svg';

let config = require('../config.json');

export default class PreLogin extends Component {
  render() {
    return (
      <div className="prelogin">
        <header className="App-header">
          <h2>
            Make playlists and see your data more easily.        </h2>
          <a href={config.backend_hostname + 'login'}>Login to Spotify</a>
      </header>
      </div>
    )
  }
}
