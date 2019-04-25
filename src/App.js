import React, { Component } from 'react';
import './App.css';
import Header from './components/Header'
import InputForm from './components/InputForm';
import Footer from './components/Footer';


class App extends Component {

  render() {
    return (
      <div className="App">
        <Header/> 
        <InputForm/>
        <Footer/>
      </div>
    );
  }
  
}

export default App;
