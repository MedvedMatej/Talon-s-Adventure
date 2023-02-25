const express = require('express');
const fs = require('fs');
const ngrok = require('ngrok');

const { createCipheriv, createDecipheriv } = require('crypto');
const key = 'Ae7nM4dG53Lo7pA4pqr474tgf47GT5z=';
const iv = Buffer.alloc(16, 0);

const app = express();
app.use(express.json());

// Define a route that returns a JSON file
app.get('/data/:level', (req, res) => {
  const filePath = `./level_data/scoreboard_${req.params.level}.json`;
  res.sendFile(filePath, { root: __dirname });
});

app.get('/leaderboard', (req, res) => {
    const filePath = `./index.html`;
    res.sendFile(filePath, { root: __dirname });
});

app.post('/save-score', (req, res) => {
    // Decrypt the data
    const encryptedMessage = Buffer.from(req.body["data"], 'hex');
    const decipher = createDecipheriv('aes-256-cbc', key, iv);
    let decryptedMessage = decipher.update(encryptedMessage);
    let data = Buffer.concat([decryptedMessage, decipher.final()]).toString('utf8');
    data = JSON.parse(data);
    console.log(data)

    
    //Validate the data
    const [minutes, seconds] = data.data.time.split(':').map(Number);
    if (data.level < 1 || data.level > 10 || data.data.deaths < 0 || minutes < 0 || seconds <= 0) {
        res.sendStatus(400);
        return;
    }
 
    // Save the data to a file
    const filePath = `./level_data/scoreboard_${data.level}.json`;
    fs.readFile(filePath, (err, fileData) => {
        if (err) {
          console.error(err);
          res.sendStatus(500);
          return;
        }
    
        // Parse existing data as JSON
        const existingData = JSON.parse(fileData);
    
        // Append new data to existing data
        existingData.push(data.data);
    
        // Write updated data back to file
        fs.writeFile(filePath, JSON.stringify(existingData), (err) => {
          if (err) {
            console.error(err);
            res.sendStatus(500);
            return;
          }
          res.sendStatus(200); // Send success response
        });
      });
  
});

// Start the server
app.listen(3000, () => {
  console.log('Server listening on port 3000');
});

ngrok.connect({
    proto : 'http',
    addr : process.env.PORT,
}, (err, url) => {
    if (err) {
        console.error('Error while connecting Ngrok',err);
        return new Error('Ngrok Failed');
    }
});