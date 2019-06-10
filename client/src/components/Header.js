import React, { Component } from 'react'
import socketIOClient from "socket.io-client";

var socket;
class Header extends Component {
  constructor() {
    socket = socketIOClient.connect();
  }
  render() {
    return (
      <div>
        <h1 className="display-4"><i class="fas fa-spider"></i>WEB CRAWLER</h1>
      </div>
    )
  }
}

export default Header
