import React, { Component } from 'react';
import { Button, Form, FormGroup, Label, Input, FormText, Containter, Row, Col } from 'reactstrap';
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
        ranged:
        {

        }
        // playlist_size:-1,
        // artists: ''
        // genres:''
      },
      genre_options:['rap',
                     'pop',
                     'pop rap'],
      rangedParamsList: ['Release Date', 'Liked Date','Tempo','Acousticness',
                         'Danceability','Energy','Instrumentalness','Valence'],
      submit_message: ''
    }
    this.handleChange = this.handleChange.bind(this);
    this.submit = this.submit.bind(this);
    this.rangedHandleChange = this.rangedHandleChange.bind(this);
  }

  handleChange(event)
  {
    let param_id = event.target.id;
    let value = event.target.value;
    //this.setState((name, value) => {console.log(name,value); return {name: value}})
    let params = this.state.params;
    params[param_id] = value;
    this.setState({params: params});
    console.log('onChange method called!',event.target.id,event.target.value);
    console.log('state:',this.state)
  }

  rangedHandleChange(event)
  {
    let ranged_params = this.state.params.ranged;
    let param_id = event.target.id;
    let param_bound = event.target.name;
    let value = event.target.value;
    if (!(Object.keys(ranged_params).includes(param_id)))
    {
      ranged_params[param_id] = {[param_bound]:value};
    }
    else
    {
      ranged_params[param_id][param_bound] = value;
    }
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
      body: JSON.stringify({params:this.state.params,
                            access_token:localStorage.getItem("access_token"),
                            uid:localStorage.getItem("uid")}), // body data type must match "Content-Type" header
  })
  .then(response => response.json())
  .then(response =>
    {
      console.log(response);
      if ((response.snapshot_id === null) || (response.snapshot_id === undefined))
      {
        this.setState({submit_message: "An error occurred."});
      }
      else
      {
        this.setState({submit_message: "Playlist created!"});
      }
      console.log(this.state);
    })
  .catch(error =>
    {
      this.setState({submit_message: "An error occurred.  Make sure you have logged in to Spotify first."});
      console.log("error caught!",this.state,error);
    });
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
            <Input type="textarea" name="playlist_size" id="playlist_size" onChange={this.handleChange}/>
          </FormGroup> 

          <FormGroup>
            <Label for="exampleText">Artists</Label>
            <Input type="textarea" name="artists" id="artists" onChange={this.handleChange}/>
          </FormGroup>

          <FormGroup>
            <Label for="exampleText">Genres</Label>
            <Input type="textarea" name="genres" id="genres" onChange={this.handleChange} />
          </FormGroup>          
          {
           this.state.rangedParamsList.map(key => 
            <div>
              {key} <p id={key.toLowerCase().replace(' ','_') + "_format"} className="format">(YYYY-MM-DD)</p>
              <Row>
                <Col className="ranged-input">
                  <FormGroup>
                    <Label for="exampleText">Minimum </Label>
                    <Input type="textarea" name="lower" id={(key).toLowerCase().replace(' ','_')} onChange={this.rangedHandleChange} />
                  </FormGroup>
                </Col>
                <Col className="ranged-input">
                  <FormGroup>
                    <Label for="exampleText">Maximum </Label>
                    <Input type="textarea" name="upper" id={(key).toLowerCase().replace(' ','_')} onChange={this.rangedHandleChange} />
                  </FormGroup>
                </Col>
              </Row>
           </div>)
          } 

          {/* <FormGroup>
            <Label for="exampleSelectMulti">Genres</Label>
            <Input type="textarea" name="genres" id="genres" onChange={this.handleChange} />
          </FormGroup> */}
        
        
      </Form>

      <Button onClick={this.submit}>Submit</Button>
      <div className="submit-message">
        {this.state.submit_message}
      </div>
      </div>
      </div>
      </div>
    )
  }
}
