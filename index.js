
const express = require('express');
require('dotenv').config();

const app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
const port = process.env.PORT || 5000;
var path = require('path');
app.use(express.static(path.join(__dirname, 'client/build')));

var exchange = 'crawl'; //exchange name
var url = process.env.CLOUDAMQP_URL || "amqp://localhost";
var open = require('amqplib').connect(url);

// socket.io setup
var http = require('http').Server(app);
var io = require('socket.io')(http);


// AWS S3 setup
var AWS = require('aws-sdk');
AWS.config.update({region:'us-east-2'});
var s3 = new AWS.S3({region:"'us-east-2'"}); // removed parameter: {apiVersion: '2006-03-01'}

// Attempt to get crawl log from S3
async function getCrawlAndEmit(socket,filename) {
  var params = {Bucket:process.env.S3_BUCKET, Key:String(filename)}; // , $waiter:{delay:5,maxAttempts:20}
  try {
    const res = await s3.getObject(params, function(err,data){
      if (err) {
        console.log(err, err.stack);
        socket.emit("notFound", '-1');
      }
      else{
        console.log('getCrawl successfully retrieved' + filename);
        res = data.Body.toString('ascii');
        socket.emit("found", res);
      } 
    });
    //res.send(res);   

  } catch (error) {
    console.error(`Error: ${error.code}`);
  }
}


// create a GET route
app.get('/', (req, res) => {
  res.render("index.html");
});


app.post('/', (req, res)=>{
  var weba = JSON.stringify(req.body.website);
  var depa = req.body.depth;
  var key = JSON.stringify(req.body.keyword);
  var qkee = JSON.stringify(req.body.searchType);
  var argList = '{ "website":' + weba + ', "depth":' + depa + ', "keyword":' + key + ', "searchType":' + qkee +'}';
  console.log(argList);

  open.then(function(conn) {
    var ok = conn.createChannel();
    ok = ok.then(function(ch) {
      ch.consume('amq.rabbitmq.reply-to', function(msg) {
        console.log('reply: ' + msg.content);
        
        let interval = 5000;

        io.on('connect', function(socket) {
          console.log('Client connected');
          var foo = setInterval( () => {
            getCrawlAndEmit(socket,msg.content);
          }, interval);
          socket.on('confirmed', () => {
            clearInterval(foo);
          });
          socket.on('disconnect', function(){ 
            console.log('Client disconnected');
          });
        });

      }, {
        noAck: true
      });
      ch.assertQueue('search');
      ch.sendToQueue('search', Buffer.from(argList), {replyTo: 'amq.rabbitmq.reply-to'});

    });
    return ok;
  }).then(null, console.warn);
  

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

