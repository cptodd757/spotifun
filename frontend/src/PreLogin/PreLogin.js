import React, { Component } from 'react';
import './PreLogin.css';
import logo from '../logo.svg';

export default class PreLogin extends Component {
  render() {
    return (
      <div className="prelogin">
        <header className="App-header">
          <h2>
            Make playlists and see your data more easily.        </h2>
          <a href="http://localhost:359/login">Login to Spotify</a>
      </header>
      </div>
    )
  }
}
