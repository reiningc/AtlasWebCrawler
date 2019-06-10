import React, { Component } from 'react';
import './App.css';
import {Router, Route} from 'react-router-dom'
import HomeScreen from './screens/HomeScreen';
import Results from './screens/Results';
import Test from './screens/Test';

import history from './history'

import socketIOClient from "socket.io-client";

class App extends Component {
  constructor() {
    super();
    this.state = {
      response: false,
      endpoint: process.env.HOST+":"+process.env.PORT
    };
  }

  componentDidMount(){
    const { endpoint } = this.state;
    const socket = socketIOClient(endpoint);
    socket.on('found', (data) => {
      console.log('in react "found" listener. received data: '+ data);
      this.setState({data: data.json(), loading: false});
      socket.emit('confirmed', '0');
      console.log('react found listener emits "confirmed"');
    });
  }
  
  render() {
    return (
      <Router history={history}>
        <div className="App">
          <Route exact path="/" component={HomeScreen}/>
          <Route exact path="/results" component={Results} />
        </div>
      </Router>
    );
  }
  
}

export default App;
