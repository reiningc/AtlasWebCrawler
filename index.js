
const express = require('express');
require('dotenv').config();

const app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(__dirname + '/public'));
app.set('port', process.argv[2]);
var path = require('path');




// create a GET route
app.get('/', (req, res) => {
  res.render("index");
});


app.post('/', (req, res)=>{
  console.log(req.body);
  var spawn = require("child_process").spawn;
  const depthCrawl = spawn('python',["./scripts/df_crawl.py", 
  req.body.website, req.body.depth]);
  depthCrawl.on('exit', function (code, signal) {
    depthCrawl.stdout.pipe(process.stdout);
    console.log('child process exited');
    res.sendFile(path.join(__dirname, '/scripts/logs', 'crawl.log'));
  });
  
  
});



app.use(function (req, res) {
  res.status(404);
  res.send('404');
});

app.use(function (err, req, res, next) {
  console.error(err.stack);
  res.status(500);
  res.send('500');
});

app.listen(app.get('port'), function () {
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});


