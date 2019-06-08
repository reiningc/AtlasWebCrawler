
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
function getCrawl(socket, filename) {
  // s3 access file
  var params = {Bucket:process.env.S3_BUCKET, Key:String(filename)}; // , $waiter:{delay:5,maxAttempts:20}
  var crawlSuccess = false;
  var maxAttempts = 20;
  var attempt = 0;
  var res = null;
  while (!crawlSuccess && attempt < maxAttempts) {
    // Check for file using headObject, if no error received, then get file with getObject
    s3.headObject(params, function(err, metadata){
      if(!err){
        s3.getObject(params, function(err,data){
          if (err) console.log(err, err.stack);
          else{
            console.log(data.Body.toString('ascii'));
            if (data.Body.toString('ascii'))
            res = data.Body.toString('ascii');
            crawlSuccess = true;
          } 
        });
      }
    });
    sleep(5000);
    socket.emit("FromAPI", 'just woke up! hello!!!'); 
    attempt += 1;
  }
  
  return res;
}

async function getCrawlAndEmit(socket,filename) {
  try {
    const res = await getCrawl(socket,filename);
    
    /*s3.waitFor('objectExists',params, function(err,data){
      if(err) console.log(err,err.stack);
      else{
        console.log('got it!');
        console.log('waitFor data received: ' + data);
        // add s3.getObject
      }
    });
    */
    res.send(res);
    
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
        
        //let interval;

        io.on('connection', function(socket) {
          console.log('Client connected');
          //if(interval) {
          //  clearInterval(interval);
          //}
          //interval = setInterval(() => getCrawlAndEmit(socket, msg.content), 10000);
          getCrawlAndEmit(socket,msg.content);
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

