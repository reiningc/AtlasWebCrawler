import React, { Component } from 'react';
import { ForceGraph2D, ForceGraph3D, ForceGraphVR } from 'react-force-graph';
import {Router, Route, Link} from 'react-router-dom';
import loading from '../images/loading.gif';
import socketIOClient from 'socket.io-client';

class Results extends Component {
    constructor(props){
        super(props);
        this.state ={
            // data that will be displayed
            // data: {},
            loading: true,
            data: {
                "nodes": [ 
                    { 
                      "id": "id1", // used to make the link
                      "name": "name1", // what will be displayed on node hover
                      "link" : "https://www.google.com", // what it will link to when clicked
                      "keyword" : "true" // used to determine if the node should be highlighted

                    },
                    { 
                        "id": "id2",
                        "name": "name2",
                      //   "val": 10,
                        "link" : "https://www.youtube.com",
                        "keyword" : "false" 
                      },],
                      "links": [
                        {
                            "source": "id1",
                            "target": "id2"
                        },]
                }

        }
    }
    
    componentDidMount = () =>{
        const { endpoint } = this.state;
        const socket = socketIOClient(endpoint);
        socket.on('found', (data) => {
            this.setState({data: data.json(), loading: false});
            socket.emit('confirmed', '0');
        });
        fetch('/', {
            method: 'POST',
            // params passed in through history props
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.props.history.location.state.param)
        }).catch(error =>
            console.log(error)
        )

    }


  render() {
    
    return (
      <div>
          <div style={{backgroundColor: "black", paddingTop: "1%", paddingBottom: "1%"}}>
            <h1 style={{color: "white"}}>Crawl Results</h1>
          </div>

        {/* Gives user the option to conduct a new crawl */}
          <div style={{padding: "1% 0 0"}}>
                <Link to='/'>
                <button className="btn btn-primary">NEW CRAWL
                </button>
                
                </Link>

            </div>

        <div style={{paddingTop: "3%"}}>


        {/* 
            NPM package to display the results
            Documentation at: https://github.com/vasturiano/react-force-graph
        */}
        {
            !this.state.loading? 
            <ForceGraph2D
            graphData={this.state.data}
            height={500}
            nodeAutoColorBy="keyword"
            backgroundColor="grey"
            showNavInfo="true"
            onNodeClick={(node) => {window.location.assign(node.link)}}
            />
            :
            // loading spinner
            <div >
                <img src={loading} style={{width: "50%", height: "50%"}}/>
            </div>
            
        }
        {/* 
            Legend that tells the user about the graph
        */}
            <div className="container">
                <div style={{border: "1px solid black"}}>
                    <div style={{backgroundColor: "black"}}>
                        <h1 style={{color: "white"}}>LEGEND</h1>
                    </div>
                    <div>
                        <div style={{display: "inline"}}>
                            <span className="dot" style={{
                                height: "25px",
                                width: "25px",
                                border: "1px solid black",
                                backgroundColor: "#cce6ff",
                                borderRadius: "50%",
                                display: "inline-block",
                            }}></span>
                            <h3 style={{display:"inline-block", paddingLeft:"2%"}}>Contain key words</h3>

                            <br></br>

                            <span className="dot" style={{
                                height: "25px",
                                width: "25px",
                                border: "1px solid black",
                                backgroundColor: "#3399ff",
                                borderRadius: "50%",
                                display: "inline-block",
                            }}></span>
                            <h3 style={{display:"inline-block", paddingLeft:"2%"}}>Does not contain key words</h3>

                        </div>
                        <div>
                            <h3>Note: Double clicking on node will redirect you to website</h3>
                        </div>
                    </div>
                </div>
            </div>
            <br></br>

        </div>
      </div>
    )
  }
}

export default Results
