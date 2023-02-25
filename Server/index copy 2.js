const express = require('express');
const app = express();

app.use(express.text());
//app.use(express.urlencoded({ extended: true }));

app.post('/save-score', (req, res) => {
  const text = req.body;
  console.log(text);
  res.send('Received text: ' + text);
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});
