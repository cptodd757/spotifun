import React, { Component } from 'react';
import { Button, Form, FormGroup, Label, Input, FormText } from 'reactstrap';
import NavbarComponent from '../NavbarComponent/NavbarComponent.js';
import { Nav } from 'react-bootstrap';
import './PlaylistCreator.css';

export default class PlaylistCreator extends Component {

  constructor()
  {
    super();
    this.state = {
      params: 
      {      
        playlist_size:-1,
        artists: '',
        genres:''
      },
      genre_options:['rap',
                     'pop',
                     'pop rap']
    }
    this.handleChange = this.handleChange.bind(this)
    this.submit = this.submit.bind(this)
  }

  handleChange(event)
  {
    let param_name = event.target.name;
    let value = event.target.value;
    //this.setState((name, value) => {console.log(name,value); return {name: value}})
    let params = this.state.params;
    params[param_name] = value;
    this.setState({params: params});
    console.log('onChange method called!',event.target.name,event.target.value);
    console.log('state:',this.state)
  }

  submit()
  {
    const submit_url = 'http://localhost:359/create_playlist';
    fetch(submit_url, {
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
      body: JSON.stringify(this.state.params), // body data type must match "Content-Type" header
  })
  .then(response => response.json());
  }

  render() {
    return (

      <div className="playlistcreator">
        <NavbarComponent>

        </NavbarComponent>
        <div className="wrapper">
        <div className="card">
        <div className="title">
          Automatically create a playlist based on the information you specify below.
          </div>
          <br></br>
        <Form>
          <FormGroup>
            <Label for="exampleText">Playlist Size</Label>
            <Input type="textarea" name="playlist_size" id="playlist_size" onChange={this.handleChange} />
          </FormGroup>

          <FormGroup>
            <Label for="exampleText">Artists</Label>
            <Input type="textarea" name="artists" id="artists" onChange={this.handleChange} />
          </FormGroup>
          
          <FormGroup>
            <Label for="exampleSelectMulti">Genres</Label>
            <Input type="textarea" name="genres" id="genres" onChange={this.handleChange} />
          </FormGroup>
        
        
      </Form>

      <Button onClick={this.submit}>Submit</Button>
      </div>
      </div>
      </div>
    )
  }
}
