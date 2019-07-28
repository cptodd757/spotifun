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
     access_token:'asdf'
   }
   this.clicked = this.clicked.bind(this)
 }

componentDidMount()
{
  
  //this.setState({access_token:''});
  const values = queryString.parse(this.props.location.search);
  console.log(values.code) // "top"
  const url = 'http://localhost:359/get_token'
  let response_data = {};
  fetch(url, 
    {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, cors, *same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: 
      {
          'Content-Type': 'application/json',
          // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify({'code': values.code}), // body data type must match "Content-Type" header
    })
  .then(response => 
    {
      response_data = response.json(); 
      return response_data;
    })
  .then(response =>
    { 
      console.log(response);
    
      this.setState({access_token : response.access_token});
      localStorage.setItem("access_token",response.access_token)
      //console.log(headers);
      console.log(localStorage);

      const user_url = 'https://api.spotify.com/v1/me';
      const headers = {"Authorization":"Bearer " + response.access_token};
      return fetch(user_url,
              {
                method: 'GET',
                headers: headers
              })
              .then(response => 
                {
                  response_data = response.json(); 
                  return response_data;
                })
              .then(response =>
                {
                  localStorage.setItem("uid",response.id);
                  console.log(localStorage);
                  const url = 'http://localhost:359/compile_liked_songs';

                  return fetch(url,
                          {
                            method: 'POST',
                            //headers: headers,
                            body: JSON.stringify({access_token: localStorage.getItem("access_token"),
                                                  uid: response.id})
                          })
                          .then(response => 
                            {
                              console.log(response.json());
                            })
                })
    })
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
        {this.state.access_token}
        <Button onClick={this.clicked}>

        </Button>
      </div>
    )
  }
}
