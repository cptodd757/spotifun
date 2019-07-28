import React, { Component } from 'react';

import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import PreLogin from '../PreLogin/PreLogin.js';
import Home from '../Home/Home.js';
import PlaylistCreator from '../PlaylistCreator/PlaylistCreator.js';

export default class AppRouter extends Component {
  render() {
    return (
      <Router>
        <div>
          <Route path="/home" component={Home} />
          <Route exact path="/" component={PreLogin}/>
          <Route path="/playlist_creator" component={PlaylistCreator}/>
        </div>
      </Router>
    );
  }
}
