import React, { Component } from 'react'
import history from '../history'
import {Router, Route, Redirect} from 'react-router-dom'
import Results from '../screens/Results';


class InputForm extends Component {
    constructor() {
        super();
        this.state = {
            data: null,
            website: "",
            searchType: "bfs",
            depth: 0,
            keyword: "",
        };
    }
    
    //   componentDidMount() {
    //     // Call our fetch function below once the component mounts
    //   this.callBackendAPI()
    //     .then(res => this.setState({ data: res.express }))
    //     .catch(err => console.log(err));
    // }
      // Fetches our GET route from the Express server. (Note the route we are fetching matches the GET route from server.js
    // callBackendAPI = async () => {
    //   const response = await fetch('/express_backend');
    //   const body = await response.json();
    
    //   if (response.status !== 200) {
    //     throw Error(body.message) 
    //   }
    //   return body;
    // };
    callBackendAPI= () => {

        let param = {};
        param["website"] = this.state.website;
        param["searchType"] = this.state.searchType;
        param["depth"] = this.state.depth;
        param["keyword"] = this.state.keyword;
        
        // return <Results param={param}/>

        // let results={}

        // fetch('http://localhost:5000/', {
        //     method: 'POST',
        //     body: param
        // }).then((response)=>
        //     response.json()
        // ).then(data=>

        //     // console.log(data)
        //     // results = Object.assign({}, data)
        //     this.setState({data: data})
        //     // results=data

            
            
        //     ).catch(error =>
        //         console.log(error)
        //         )
        
        
        fetch('/' + param.searchType, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ param })
          });
        history.push('/results', {param})
    }
    
    setWebsite=(e)=> {
        this.setState({website: e.target.value});
    }

    setSearchType=(e)=> {
        this.setState({searchType: e.target.value});
    }

    setDepth=(e)=> {
        this.setState({depth: e.target.value});
    }

    setKeyWord=(e)=> {
        this.setState({keyword: e.target.value});
    }

  render() {
    return (
      <div>
        {/* input form */}
        {/* <form action="http://localhost:5000" method="post" className="container"> */}
        <form className="container">


            {/* starting address */}
            <div className="form-group row">
                <div className="col-sm">
                    <label>Starting address for crawl:</label>
                </div>
                <div className="col-sm">
                    <input type="url" className="form-control col-xs-4" name="website" onChange={(e)=>this.setWebsite(e)}/>
                </div>
            </div>

            {/* type of search */}
            <div className="form-group">
                <div className="row">
                    <div className="col-md">
                        <label className="radio-inline">Select Search Type:</label>
                    </div>
                    <div className="col-md">
                        <input type="radio" name="optradio" style={{marginRight: "25px"}} value="bfs" defaultChecked onChange={(e)=>this.setSearchType(e)}/> 
                        <label className=""> Breadth First Search</label>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md"></div>
                    <div className="col-md">
                        <input type="radio" name="optradio" style={{marginRight: "36px"}} value="dfs" onChange={(e)=>this.setSearchType(e)}/> 
                        <label className=""> Depth First Search</label>
                    </div>
                </div>
            </div>

            {/* Max number of links */}
            <div className="form-group row">
                <div className="col-sm">
                    <label >Select Maximum Number of Links to Follow: </label>
                </div>
                <div className="col-sm">
                    <input type="number" className="col-xs-4" name="depth" min="0" onChange={(e)=>this.setDepth(e)}/>
                </div>
            </div>

            {/* Key word */}
            <div className="form-group row">
                <div className="col-sm">
                    <label >Enter a word that when encountered will stop crawl:</label>
                </div>
                <div className="col-sm">
                    <input type="text" className="col-xs-4" name="keyword" onChange={(e)=>this.setKeyWord(e)}/>
                </div>
            </div>

            {/* submit button */}
            <div className="row">
                <div className="col-sm"></div>
                <div className="col-sm">
                    <button type="submit" onClick={()=>this.callBackendAPI()}className="btn btn-primary">Submit</button>
                </div>
                <div className="col-sm"></div>

            </div>
        </form>
      </div>
    )
  }
}

export default InputForm
