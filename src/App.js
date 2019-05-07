import React, { Component } from 'react';
import './App.css';
import {Router, Route} from 'react-router-dom'
import HomeScreen from './screens/HomeScreen';
import Results from './screens/Results';

import history from './history'

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
