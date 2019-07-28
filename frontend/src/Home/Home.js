import React, { Component } from 'react';
import queryString from 'query-string';
import { Button } from 'reactstrap';
import NavbarComponent from '../NavbarComponent/NavbarComponent.js';

import './Home.css';
import { Nav } from 'react-bootstrap';

export default class Home extends Component {

 constructor()
 {
   super();
   this.state = {
     api_key:'asdf'
   }
   this.clicked = this.clicked.bind(this)
 }

componentDidMount()
{
  
  //this.setState({api_key:''});
  const values = queryString.parse(this.props.location.search);
  console.log(values.code) // "top"
  const url = 'http://localhost:359/get_token'
  let response_data = {};
  fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, cors, *same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
        'Content-Type': 'application/json',
        // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({'code': values.code}), // body data type must match "Content-Type" header
})
.then(response => 
  {response_data = response.json(); return response_data;}).then(response =>
   
   { console.log(response);
    const url = 'http://localhost:359/compile_liked_songs';
    //const headers = {"Authorization":"Bearer " + response.access_token};
    this.setState({api_key : response.access_token});
    //console.log(headers);
    return fetch(url,{
      method: 'POST',
      //headers: headers,
      body: {access_token: response.access_token}
    }).then(response => {console.log(response.json())})
  }
    )
  //console.log(values.origin) // "im"
  console.log('yo');
}

clicked()
{
  console.log(this.state);
}

  render() {
    return (
      <div className="home">
        <NavbarComponent>

        </NavbarComponent>
        {this.state.api_key}
        <Button onClick={this.clicked}>

        </Button>
      </div>
    )
  }
}
