
const express = require('express');
require('dotenv').config();

const app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
const port = process.env.PORT || 5000;
var path = require('path');
app.use(express.static(path.join(__dirname, 'client/build')));

var q = 'tasks';

var url = process.env.CLOUDAMQP_URL || "amqp://localhost";
var open = require('amqplib').connect(url);

// create a GET route
app.get('/', (req, res) => {
  res.render("index.html");
});


app.post('/dfs', (req, res)=>{
  console.log(req.body.param);
  var weba = req.body.website;
  var depa = req.body.depth;
  var key = req.body.keyword;
  var argList = '{ "website":' + weba + ' "depth":' + depa + ' "keyword":' + key + '}';
  console.log(argList);
  open.then(function(conn) {
    var ok = conn.createChannel();
    ok = ok.then(function(ch) {
      ch.assertQueue(q);
      ch.sendToQueue(q, Buffer.from(argList));
    });
    return ok;
  }).then(null, console.warn);
});


app.post('/bfs', (req, res)=>{
  
  console.log(req.body.website);
  
  
  
});


if (process.env.NODE_ENV === 'production') {
  // Serve any static files
  app.use(express.static(path.join(__dirname, 'client/build')));
  // Handle React routing, return all requests to React app
  app.get('*', function(req, res) {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
  });
}


app.use(function (req, res) {
  res.status(404);
  res.send('404');
});

app.use(function (err, req, res, next) {
  console.error(err.stack);
  res.status(500);
  res.send('500');
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`)
});

