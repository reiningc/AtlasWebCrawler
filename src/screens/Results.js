import React, { Component } from 'react'
import { ForceGraph2D, ForceGraph3D, ForceGraphVR } from 'react-force-graph';
import {Router, Route, Link} from 'react-router-dom'


class Results extends Component {
    constructor(props){
        super(props);
        this.state ={
            // data that will be displayed
            data: {
                "nodes": [ 
                    { 
                      "id": "id1", // used to make the link
                      "name": "name1", // what will be displayed on node hover
                    //   "val": 1,  // this will affect node size
                      "link" : "https://www.google.com", // what it will link to when clicked
                      "keyword" : "true" // used to determine if the node should be highlighted

                    },
                    { 
                      "id": "id2",
                      "name": "name2",
                    //   "val": 10,
                      "link" : "https://www.youtube.com",
                      "keyword" : "false" 
                    },
                    { 
                        "id": "id3",
                        "name": "name3",
                        // "val": 103,
                        "link" : "https://www.espn.com",
                        "keyword": "true" 
                      },
                      { 
                        "id": "id4",
                        "name": "name4",
                        // "val": 103,
                        "link" : "https://www.espn.com",
                        "keyword": "true" 
                      },
                      { 
                        "id": "id5",
                        "name": "name5",
                        // "val": 103,
                        "link" : "https://www.espn.com",
                        "keyword": "false" 
                      },
                      { 
                        "id": "id6",
                        "name": "name6",
                        // "val": 103,
                        "link" : "https://www.espn.com",
                        "keyword": "true" 
                      },
                ],
                "links": [
                    {
                        "source": "id1",
                        "target": "id2"
                    },
                    {
                        "source": "id1",
                        "target": "id3"
                    },
                    {
                        "source": "id3",
                        "target": "id4"
                    },
                    {
                        "source": "id3",
                        "target": "id5"
                    },
                    {
                        "source": "id3",
                        "target": "id6"
                    },
                ]
            }
        }
    }


  render() {
    
    return (
      <div>
        <h1>Crawl Results</h1>

        <div style={{paddingTop: "3%"}}>

        {/* 
            NPM package to display the results
            Documentation at: https://github.com/vasturiano/react-force-graph
        */}
          <ForceGraph2D
            graphData={this.state.data}
            height={500}
            nodeAutoColorBy="keyword"
            backgroundColor="grey"
            showNavInfo="true"
            onNodeClick={(node) => {window.location.assign(node.link)}}
            />

        {/* 
            Legend that tells the user about the graph
        */}

            <div className="container">
                <div style={{border: "1px solid black"}}>
                    <h1>LEGEND</h1>
                    <div>
                        <div style={{display: "inline"}}>
                            <span class="dot" style={{
                                height: "25px",
                                width: "25px",
                                border: "1px solid black",
                                backgroundColor: "#cce6ff",
                                borderRadius: "50%",
                                display: "inline-block",
                            }}></span>
                            <h3 style={{display:"inline-block", paddingLeft:"2%"}}>Contain key words</h3>

                            <br></br>

                            <span class="dot" style={{
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

            {/* Gives user the option to conduct a new crawl */}
            <div>
                <Link to='/'>
                <button >NEW CRAWL
                </button>
                
                </Link>

            </div>

        </div>
      </div>
    )
  }
}

export default Results
