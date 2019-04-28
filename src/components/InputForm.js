import React, { Component } from 'react'

class InputForm extends Component {
    constructor() {
        super();
        this.state = {
            data: null
        };
    }
    
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
      <div>
        {/* input form */}
        <form action="/express_backend" method="post" className="container">
                <br/>
                <h5 className="App-intro">{this.state.data}</h5>
                <br/>
            {/* starting address */}
            <div className="form-group row">
                
                <div className="col-sm">
                    <label for="website">Starting address for crawl:</label>
                </div>
                <div className="col-sm">
                    <input type="url" className="form-control" class="col-xs-4" name="website" id="website"/>
                </div>
            </div>

            {/* type of search */}
            <div className="form-group">
                <div className="row">
                    <div className="col-md">
                        <label class="radio-inline">Select Search Type:</label>
                    </div>
                    <div className="col-md">
                        <input type="radio" name="optradio" style={{marginRight: "25px"}} checked/> 
                        <label class="radio-inline"> Breadth First Search</label>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md"></div>
                    <div className="col-md">
                        <input type="radio" name="optradio" style={{marginRight: "36px"}} /> 
                        <label class="radio-inline"> Depth First Search</label>
                    </div>
                </div>
            </div>

            {/* Max number of links */}
            <div class="form-group row">
                <div className="col-sm">
                    <label for="depth">Select Maximum Number of Links to Follow: </label>
                </div>
                <div className="col-sm">
                    <input type="number" class="col-xs-4" id="depth" min="0" name="linkNum"/>
                </div>
            </div>

            {/* Key word */}
            <div className="form-group row">
                <div className="col-sm">
                    <label for="safeword">Enter a word that when encountered will stop crawl:</label>
                </div>
                <div class="col-sm">
                    <input type="text" class="col-xs-4" id="safeword" name="keyword"/>
                </div>
            </div>

            {/* submit button */}
            <div className="row">
                <div className="col-sm"></div>
                <div className="col-sm">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
                <div className="col-sm"></div>

            </div>
        </form>
      </div>
    )
  }
}

export default InputForm
