const express = require('express');
require('dotenv').config();

const app = express();

const port = process.env.PORT || 5000;

// create a GET route
app.get('/express_backend', (req, res) => {
  res.send({ express: 'YOUR EXPRESS BACKEND IS CONNECTED TO REACT' });
});

app.post('/express_backend', (req, res, next)=>{
  res.send({express: 'received post request'});
});


app.use(function (req, res) {
  res.status(404);
  res.render('404');
});

app.use(function (err, req, res, next) {
  console.error(err.stack);
  res.status(500);
  res.render('500');
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`)
});