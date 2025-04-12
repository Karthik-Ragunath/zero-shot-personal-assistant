const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 8080;
const UPLOAD_DIR = path.join(__dirname, 'uploads');

const server = http.createServer((req, res) => {
  // Check if this is a POST request to save audio
  if (req.method === 'POST' && req.url === '/save-audio') {
    let data = [];
    
    req.on('data', chunk => {
      data.push(chunk);
    });
    
    req.on('end', () => {
      const buffer = Buffer.concat(data);
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `recording-${timestamp}.webm`;
      const filePath = path.join(UPLOAD_DIR, filename);
      
      fs.writeFile(filePath, buffer, (err) => {
        if (err) {
          console.error('Error saving file:', err);
          res.statusCode = 500;
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify({ success: false, error: 'Error saving file' }));
        } else {
          console.log(`File saved: ${filename}`);
          res.statusCode = 200;
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify({ success: true, filename }));
        }
      });
    });
    
    return;
  }
  
  // Handle GET requests
  if (req.method !== 'GET') {
    res.statusCode = 405;
    res.end('Method Not Allowed');
    return;
  }

  // Set the URL path, defaulting to index.html
  const filePath = req.url === '/' 
    ? path.join(__dirname, 'index.html') 
    : path.join(__dirname, req.url);

  // Get the file extension
  const extname = path.extname(filePath);
  
  // Set content type based on file extension
  let contentType = 'text/html';
  switch (extname) {
    case '.js':
      contentType = 'text/javascript';
      break;
    case '.css':
      contentType = 'text/css';
      break;
    case '.json':
      contentType = 'application/json';
      break;
    case '.png':
      contentType = 'image/png';
      break;
    case '.jpg':
    case '.jpeg':
      contentType = 'image/jpeg';
      break;
    case '.wav':
      contentType = 'audio/wav';
      break;
    case '.webm':
      contentType = 'audio/webm';
      break;
    case '.mp3':
      contentType = 'audio/mpeg';
      break;
  }

  // Read the file
  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        // File not found
        res.statusCode = 404;
        res.end('Not Found');
      } else {
        // Server error
        res.statusCode = 500;
        res.end(`Server Error: ${err.code}`);
      }
    } else {
      // Success: serve the file
      res.statusCode = 200;
      res.setHeader('Content-Type', contentType);
      res.end(content);
    }
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running at http://0.0.0.0:${PORT}/`);
  console.log(`Press Ctrl+C to stop the server`);
});