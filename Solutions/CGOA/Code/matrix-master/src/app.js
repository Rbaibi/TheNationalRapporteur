import express from 'express';
const app = express();

import pdfparser from './Modules/PdfParser';

const hostname = '127.0.0.1';
const port = 3000;

app.get('/', (req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  let pdf = "test";//await pdfparser.parsePdf("c:/test");
  res.send(`Hello ${pdf}`);
});

app.get('/about', (req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.send('About page');
});

app.listen(port, hostname, () => console.log(`Server running at http://${hostname}:${port}/`));
