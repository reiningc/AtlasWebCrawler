import React, { Component } from 'react';
import './App.css';
import TestComponent from './components/testcomponent';

class App extends Component {
  render() {
    return (
      <div className="App">
        <TestComponent></TestComponent>
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
