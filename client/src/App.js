import React, { Component } from 'react';
import './App.css';
import {Router, Route} from 'react-router-dom'
import HomeScreen from './screens/HomeScreen';
import Results from './screens/Results';
import Test from './screens/Test';

import history from './history'

const io = require('socket.io-client');
const socket = io();

class App extends Component {

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
