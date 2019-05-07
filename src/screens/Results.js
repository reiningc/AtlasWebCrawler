import React, { Component } from 'react'

class Results extends Component {
    constructor(props){
        super(props);
        this.state ={
            dummydata: 
                { start: 
                    {  
                        title: "Test1", 
                        keyword: true, 
                        url: "www.start.com", 
                        links: [
                                { 
                                    title: "google", 
                                    keyword: false, 
                                    url: "https://www.google.com", 
                                    links: [
                                            { 
                                                title: "youtube", 
                                                keyword: true, 
                                                url: "https://www.youtube.com", 
                                                links: [
                                                    { 
                                                        title: "google", 
                                                        keyword: false, 
                                                        url: "https://www.google.com", 
                                                        links: [
                                                                { 
                                                                    title: "youtube", 
                                                                    keyword: true, 
                                                                    url: "https://www.youtube.com", 
                                                                    links: []
                                                                }
                                                        ]
                                                    }
                                                ]
                                            },
                                            { 
                                                title: "stack overflow", 
                                                keyword: true, 
                                                url: "https://www.stackoverflow.com", 
                                                links: [
                                                    { 
                                                        title: "oregon state", 
                                                        keyword: false, 
                                                        url: "https://www.oregonstate.com", 
                                                        links: []
                                                    }
                                                ]
                                            }
                                    ]
                                },
                                { 
                                    title: "facebook", 
                                    keyword: false, 
                                    url: "https://www.facebook.com", 
                                    links: [
                                            { 
                                                title: "espn", 
                                                keyword: true, 
                                                url: "https://www.espn.com", 
                                                links: []
                                            }
                                    ]
                                }
                        ]
                    }
                }
        }
    }

    displayObj = (obj) => {
        
        if(obj.links.length != 0)
        {
            return obj.links.map((test) => (
                <ul>
                    <li className="" style={test.keyword ? {color:"red"} : null}>
                        <div className="border border-primary rounded-circle" 
                                style={{ width: "200px", height: "200px", 
                                        overflow: "hidden", whiteSpace: "nowrap", 
                                        textOverflow: "ellipsis", paddingTop: "4%"
                                        }}>
                            <div style={{margin: "0 auto"}}>
                                {test.title}
                                <div>
                                    <a href={test.url}>{test.url}</a>
                                </div>
                            </div>
                        </div>
                    </li>
                    {
                        this.displayObj(test)
                    }
                </ul>
            ))
        }
    }
  render() {

    let data = <div>
        <ul>
            <li>
                        <div className="border border-primary rounded-circle" 
                                style={{ width: "200px", height: "200px", 
                                        overflow: "hidden", whiteSpace: "nowrap", 
                                        textOverflow: "ellipsis", paddingTop: "4%"
                                        }}>
                            <div style={{margin: "0 auto"}}>
                                <h1>START</h1>
                                {this.state.dummydata.start.title}
                                <div>
                                    <a href={this.state.dummydata.start.url}>{this.state.dummydata.start.url}</a>
                                </div>
                            </div>
                        </div>
                {
                    this.displayObj(this.state.dummydata.start)
                }
            </li>
        </ul>
    </div>
    
    return (
      <div>
        {data}
      </div>
    )
  }
}

export default Results
