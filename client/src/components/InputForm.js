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
            prevSearches: [],
            displayCreateCrawl: true,
            displayPrevCrawls: false,
            apiParam: {}
        };
    }

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

        if( this.state.website != "")
        {            
            let param = {};
            param["website"] = this.state.website;
            param["searchType"] = this.state.searchType;
            param["depth"] = this.state.depth;
            param["keyword"] = this.state.keyword;


            let oldCrawls = localStorage.getItem('previousCrawls')

            //if it is empty just add new search
            if( oldCrawls == null)
            {
                let newSearch = param
                let prevSearch = []
                prevSearch.push(newSearch)
                localStorage.setItem("previousCrawls", JSON.stringify(prevSearch))
            }
            // if not empty add new to old
            else {
                // add new crawl
                let oldCrawlList = JSON.parse(localStorage.getItem("previousCrawls"))
                let newSearch = param
                oldCrawlList.push(newSearch)
                // set to local storage
                localStorage.setItem("previousCrawls", JSON.stringify(oldCrawlList))
            }

            // go to new page
            history.push('/results', {param})
        }
    }
    callBackendAPIPrevSearch = () => {
        let param = this.state.apiParam
        // only makes the api call if a search is selected
        if(Object.keys(param).length !== 0)
            // go to new page
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

    toggleCreateCrawl = () => {
        let prevState = this.state.displayCreateCrawl
        let prevCrawls = this.state.displayPrevCrawls
        this.setState({displayCreateCrawl: !prevState, displayPrevCrawls: !prevCrawls})
    }
    togglePrevCrawls = () => {
        let prevCrawls = this.state.displayPrevCrawls
        let prevState = this.state.displayCreateCrawl
        this.setState({displayPrevCrawls: !prevCrawls, displayCreateCrawl: !prevState})
    }

    setParam = (prevCrawl) => {
        this.setState({apiParam: prevCrawl})
    }

    displayPrevCrawls = () =>{
        // get previous crawls
        let oldCrawlList = JSON.parse(localStorage.getItem("previousCrawls"))

        // no previous crawls
        if( oldCrawlList == null)
            return <div style={{width: "200px", height: "200px", margin: "0 auto"}}>
                    <h2>No previous Searchs</h2>
                </div>
        else{
            
            return <div className="container">
                <div className="row" style={{paddingBottom: "3%"}}>
                        <div className="col-sm"><h3></h3></div>
                        <div className="col-sm"><h3>Website</h3></div>
                        <div className="col-sm"><h3>Search Type</h3></div>
                        <div className="col-sm"><h3>Depth</h3></div>
                        <div className="col-sm"><h3>Keyword</h3></div>
                </div>
                <fieldset class="form-group">
                {            
                    oldCrawlList.map((search) => 
                    (                    
                        <div class="">
                                <div className="row" style={{paddingBottom: "2%"}}>
                                    <div className="col-sm">
                                        <input  type="radio" name="gridRadios" id="gridRadios1" value="option1" required onClick={()=> this.setParam(search)}></input>
                                    </div>
                                    <div className="col-sm">{search.website}</div>
                                    <div className="col-sm">{search.searchType}</div>
                                    <div className="col-sm">{search.depth}</div>
                                    <div className="col-sm">{search.keyword}</div>
                                </div>
                                
                        </div>
                    )
                    )
                }
                </fieldset>

                {/* submit button */}
                <div className="row">
                    <div className="col-sm"></div>
                    <div className="col-sm">
                        <button type="submit" onClick={()=>this.callBackendAPIPrevSearch()}className="btn btn-primary">Submit</button>
                    </div>
                    <div className="col-sm"></div>

                </div>
            </div> 

        }
    }

  render() {
    return (
      <div>
        {/* input form */}
        {/* <form action="http://localhost:5000" method="post" className="container"> */}
        <div style={{ padding: " 2% 2% 2% 2%", width: "100%", height: "100%"}}>

            <ul className="nav nav-tabs">
                <li className="nav-item">
                    <button
                        className={
                            this.state.displayCreateCrawl?
                            "btn nav-link active"
                            :
                            "btn nav-link"
                        }

                    onClick={()=> this.toggleCreateCrawl()}>Create Crawl</button>
                </li>
                <li className="nav-item">
                    <button
                    className={
                        this.state.displayPrevCrawls ?
                        "btn nav-link active"
                        :
                        "btn nav-link"
                    }
                    onClick={ ()=> this.togglePrevCrawls()}
                    >Previous Crawls</button>
                </li>
            </ul>
        {
            this.state.displayCreateCrawl ?
        
            <form className="container" style={{paddingTop: "5%"}}>
                {/* starting address */}
                <div className="form-group row">
                    <div className="col-sm">
                        <label>Starting address for crawl:</label>
                    </div>
                    <div className="col-sm">
                        <input type="url" required className="form-control col-xs-4" name="website" onChange={(e)=>this.setWebsite(e)}/>
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
                        <input type="number" required placeholder="0" className="col-xs-4" name="depth"  min="0" 
                        max={
                            this.state.searchType == "bfs" ?
                            "3"
                            :
                            "10"
                        } 
                        onChange={(e)=>this.setDepth(e)}/>
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
            :
            null
        }
        {
            this.state.displayPrevCrawls ?
            <div className="container " style={{paddingTop: "5%"}}>
                {this.displayPrevCrawls()}
            </div>
            :
            null
        }
        </div>
      </div>
    )
  }
}

export default InputForm
