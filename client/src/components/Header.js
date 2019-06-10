import React, { Component } from 'react'
import socketIOClient from "socket.io-client";

var socket;
class Header extends Component {
  constructor() {
    super();
    socket = socketIOClient.connect();
    socket.on("findMe", () => {socket.emit("findMe", "header")});
  }
  render() {
    return (
      <div>
        <h1 className="display-4"><i class="fas fa-spider"></i>WEB CRAWLER</h1>
      </div>
    )
  }
}

export { Header, socket };
