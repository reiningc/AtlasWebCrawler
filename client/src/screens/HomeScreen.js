import React, { Component } from 'react'
import Header from '../components/Header'
import InputForm from '../components/InputForm';
import Footer from '../components/Footer';

export class HomeScreen extends Component {
  render() {
    return (
      // <div>
      
      <div style={{
        // backgroundImage:"url(" + "https://backgrounddownload.com/wp-content/uploads/2018/09/spider-web-corner-png-transparent-background-2.png" + ")",
        backgroundImage:"url(" + "https://cdn.clipart.email/316ce6bbac93bf029705c9131989459e_corner-spider-web-clipart-clipart-panda-free-clipart-images_900-900.svg" + ")",        
        backgroundPosition: "cover",
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: "fixed"
        }}>
        <div style={{height: "100%", paddingTop: "9%", paddingBottom: "20%", paddingLeft: "15%", paddingRight: "15%"}}>
          <div style={{
            background: "white",
            // opacity: "0.6"
            }}>
            <Header/> 
            <InputForm/>
            <Footer/>
          </div>
        </div>
      </div>
    )
  }
}

export default HomeScreen
