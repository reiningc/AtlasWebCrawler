import React, { Component } from 'react'
import Header from '../components/Header'
import InputForm from '../components/InputForm';
import Footer from '../components/Footer';

export class HomeScreen extends Component {
  render() {
    return (
      <div>
        <Header/> 
        <InputForm/>
        <Footer/>
      </div>
    )
  }
}

export default HomeScreen
