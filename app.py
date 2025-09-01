from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <html>
        <head><title>Test App</title></head>
        <body>
            <h1>Hello from App Runner!</h1>
            <p>This is a simple Flask app.</p>
            <p>If you see this, the deployment is working!</p>
        </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)