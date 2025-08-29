#!/usr/bin/env python3
"""
Ultra-simple HTTP server for App Runner testing
"""
import http.server
import socketserver
import os

PORT = int(os.environ.get('PORT', 8080))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test App</title>
        </head>
        <body>
            <h1>Hello from App Runner!</h1>
            <p>This is a simple Python HTTP server.</p>
            <p>If you see this, the basic deployment is working.</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Server running on port {PORT}")
        httpd.serve_forever()