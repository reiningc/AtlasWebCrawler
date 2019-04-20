import React, { Component } from 'react';
import './App.css';
import TestComponent from './components/testcomponent';

class App extends Component {
  state = {
    data: null
  };

  componentDidMount() {
    // Call our fetch function below once the component mounts
  this.callBackendAPI()
    .then(res => this.setState({ data: res.express }))
    .catch(err => console.log(err));
}
  // Fetches our GET route from the Express server. (Note the route we are fetching matches the GET route from server.js
callBackendAPI = async () => {
  const response = await fetch('/express_backend');
  const body = await response.json();

  if (response.status !== 200) {
    throw Error(body.message) 
  }
  return body;
};


  render() {
    return (
      <div className="App">
        <TestComponent></TestComponent>
        <br/>
          <p className="App-intro">{this.state.data}</p>
        <br/>
        <form>
        <div class="form-group"> 
        <label for="website">Starting address for crawl:</label>
        <br/>
            <input type="url" class="col-xs-4" id="website"/>
        <br/>
        <br/>
        <label class="radio-inline">Select Search Type:</label>
        <br/>
        <label class="radio-inline">
      <input type="radio" name="optradio" checked/>Breadth First Search
      </label>
      <label class="radio-inline">
        <input type="radio" name="optradio" />Depth First Search
      </label>
       <br/>
        <br/>
        <div class="form-group">
        
          <label for="depth">Select Maximum Number of Links to Follow: </label>
          <br/>
          <input type="number" class="col-xs-4" id="depth" />
        </div>
        <br/>
        <div class="col-xs-4">
          <label for="safeword">Enter a word that when encountered will stop crawl:</label>
          <br/>
          <input type="text" class="col-xs-4" id="safeword" />
          <br/>
        </div>
                </div>
            <button type="submit" class="btn btn-primary">Submit</button>
            </form>
      </div>
    );
  }
  
}

export default App;
