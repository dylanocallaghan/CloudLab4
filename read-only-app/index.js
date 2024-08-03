const express = require('express');
const mysql = require('mysql');

const app = express();
const port = 3000;

const connection = mysql.createConnection({
  host: 'db',
  user: 'root',
  password: 'example',
  database: 'myapp'
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }
  console.log('Connected to MySQL');
});

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/users', (req, res) => {
  connection.query('SELECT * FROM users', (error, results) => {
    if (error) {
      console.error('Error fetching users:', error);
      res.status(500).send('Error fetching users');
    } else {
      res.json(results);
    }
  });
});

// Remove or comment out modifying routes
/*
app.post('/users', (req, res) => {
  // Code to add a new user
});

app.put('/users/:id', (req, res) => {
  // Code to update a user
});

app.delete('/users/:id', (req, res) => {
  // Code to delete a user
});
*/

app.listen(port, () => {
  console.log(`Server running at http://0.0.0.0:${port}/`);
});

