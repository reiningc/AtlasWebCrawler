import React, { Component } from 'react'

class Footer extends Component {
    render() {
    let styling ={
        position: "fixed",
        left: "0",
        bottom: "0",
        width: "100%",
        height: "8%",
        backgroundColor: "black",
        color: "white",
        textAlign: "center"
    }

    return (
      <div>
        <div style={styling}>
            Creators: Jessica Adams, Colin Reininger, and Nathaniel Villegas
            <br></br>
            © 2019
        </div>
      </div>
    )
  }
}

export default Footer
