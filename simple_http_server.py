#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
import json
from urllib.parse import parse_qs

PORT = int(os.environ.get('PORT', 8080))

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy'}).encode())
            return
            
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test App 🧪</title>
            <style>
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    max-width: 1200px; margin: 0 auto; padding: 2rem;
                    background-color: #fafafa;
                }}
                .container {{ 
                    background: white; padding: 2rem; border-radius: 10px; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                .success {{ 
                    background: #d4edda; color: #155724; padding: 1rem; 
                    border-radius: 5px; margin: 1rem 0;
                }}
                .code {{ 
                    background: #f8f9fa; padding: 0.5rem; border-radius: 3px; 
                    font-family: monospace; border-left: 3px solid #007bff;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧪 Test App - Simple HTTP Server</h1>
                <div class="success">
                    ✅ App Runner deployment successful!<br>
                    <strong>No WebSocket dependencies!</strong>
                </div>
                
                <h2>Environment Information</h2>
                <p><strong>Python Version:</strong></p>
                <div class="code">{sys.version}</div>
                
                <p><strong>Working Directory:</strong></p>
                <div class="code">{os.getcwd()}</div>
                
                <h2>Environment Variables</h2>
                <p><strong>AWS_REGION:</strong> <code>{os.getenv('AWS_REGION', 'Not set')}</code></p>
                <p><strong>KB_ID:</strong> <code>{os.getenv('KB_ID', 'Not set')}</code></p>
                <p><strong>PORT:</strong> <code>{os.getenv('PORT', 'Not set')}</code></p>
                
                <hr>
                <div style="background: #d1ecf1; color: #0c5460; padding: 1rem; border-radius: 5px;">
                    🎉 <strong>Success!</strong> This proves App Runner can deploy Python apps.<br>
                    The deployment is working perfectly with standard HTTP only.
                </div>
                
                <p><strong>Health Check:</strong> <a href="/health">/health</a></p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        self.do_GET()  # Handle POST same as GET for now

if __name__ == "__main__":
    print(f"Starting server on port {PORT}")
    with socketserver.TCPServer(("0.0.0.0", PORT), TestHandler) as httpd:
        print(f"Server running at http://0.0.0.0:{PORT}")
        httpd.serve_forever()