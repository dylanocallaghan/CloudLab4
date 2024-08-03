const mysql = require('mysql');
const connection = mysql.createConnection({
  host: 'mysql',
  user: 'user',
  password: 'password',
  database: 'mydatabase'
});

connection.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL database');
});

