const http = require('http');

var current = null

http.createServer((request, response) => {
    if (request.method == 'POST') {
        var body = '';
        request.on('data', function(data) {
            body += data;
        })
        request.on('end', function() {
            current = body;
            console.log(body);
            response.end();
        })
    } else {
        response.end(current);
    }
})