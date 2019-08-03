import React, { Component } from 'react';
import { Button } from 'react-bootstrap';

export default class Login extends Component 
{

  constructor()
  {
    super();
  }

  clicked()
  {
    // const client_id = '81d7431ddf80433585d18cca9c08c815';
    // const scope = 'user-read-private user-read-email user-top-read';
    // const redirect_uri = 'http://3.86.203.151:3000';
    // const queryString = require('query-string')
    // const url = 'https://accounts.spotify.com/authorize?' +
    //             queryString.stringify({
    //               response_type: 'token',
    //               client_id: client_id,
    //               scope: scope,
    //               redirect_uri: redirect_uri
    //             })
    const url = 'http://54.82.235.204:4000/login';
    console.log(url)
    console.log('hello');
    //postData('http://54.82.235.204:4000/login', {answer: 42})
    //  .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
    //  .catch(error => console.error(error)); 
    fetch(url).then(response => console.log(response));

    function postData(url = '', data = {}) {
      // Default options are marked with *
      console.log( JSON.stringify(data));
        return fetch(url, {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, cors, *same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json',
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: 'follow', // manual, *follow, error
            referrer: 'no-referrer', // no-referrer, *client
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        })
        .then(response => response.json()); // parses JSON response into native JavaScript objects 
    }
  }


  render() {
    return (
      <div className="login">
          <Button onClick={this.clicked}>
            Click me to login
          </Button>
      </div>
    )
  }
}
