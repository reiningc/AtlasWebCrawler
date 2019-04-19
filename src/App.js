import React, { Component } from 'react';
import './App.css';
import TestComponent from './components/testcomponent';
import Urlbox from './components/urlentry';
class App extends Component {
  render() {
    return (
      <div className="App">
        <TestComponent></TestComponent>
        <Urlbox></Urlbox>
      </div>
    );
  }
  
}

export default App;
