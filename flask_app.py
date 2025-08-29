from flask import Flask, render_template_string, request
import os
import sys

app = Flask(__name__)

# HTML template that looks similar to Streamlit
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Test App 🧪</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 2rem;
            background-color: #fafafa;
        }
        .container { 
            background: white; 
            padding: 2rem; 
            border-radius: 10px; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .success { 
            background: #d4edda; 
            color: #155724; 
            padding: 1rem; 
            border-radius: 5px; 
            margin: 1rem 0;
        }
        .info { 
            background: #d1ecf1; 
            color: #0c5460; 
            padding: 1rem; 
            border-radius: 5px; 
            margin: 1rem 0;
        }
        .code { 
            background: #f8f9fa; 
            padding: 0.5rem; 
            border-radius: 3px; 
            font-family: monospace;
            border-left: 3px solid #007bff;
        }
        .form-group { 
            margin: 1rem 0; 
        }
        input, button { 
            padding: 0.5rem; 
            margin: 0.25rem; 
            border: 1px solid #ddd; 
            border-radius: 3px;
        }
        button { 
            background: #007bff; 
            color: white; 
            cursor: pointer;
        }
        button:hover { 
            background: #0056b3; 
        }
        .cols { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 2rem; 
            margin: 1rem 0;
        }
        hr { 
            border: none; 
            border-top: 1px solid #eee; 
            margin: 2rem 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test App - Flask Version</h1>
        <p><strong>App is running successfully!</strong></p>
        
        <div class="success">
            ✅ Deployment successful - No WebSocket needed!
        </div>

        <h2>Environment Information</h2>
        <div class="cols">
            <div>
                <strong>Python Version:</strong>
                <div class="code">{{ python_version }}</div>
            </div>
            <div>
                <strong>Working Directory:</strong>
                <div class="code">{{ working_dir }}</div>
            </div>
        </div>

        <h2>Environment Variables</h2>
        <p><strong>AWS_REGION:</strong> <code>{{ aws_region }}</code></p>
        <p><strong>KB_ID:</strong> <code>{{ kb_id }}</code></p>
        <p><strong>PORT:</strong> <code>{{ port }}</code></p>

        <hr>

        <h2>Test Form</h2>
        <form method="POST">
            <div class="form-group">
                <label><strong>Enter some text:</strong></label><br>
                <input type="text" name="test_input" value="{{ test_input or '' }}" placeholder="Type something...">
                <button type="submit">Submit</button>
            </div>
        </form>
        
        {% if form_submitted %}
        <div class="success">
            ✅ Form submitted! You entered: <strong>{{ test_input }}</strong>
        </div>
        {% endif %}

        <hr>
        
        <div class="info">
            🎉 If you can see this page completely, the App Runner deployment is working perfectly!<br>
            <strong>No WebSocket errors!</strong> This Flask app works with standard HTTP requests only.
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    form_submitted = False
    test_input = None
    
    if request.method == 'POST':
        form_submitted = True
        test_input = request.form.get('test_input', '')
    
    return render_template_string(HTML_TEMPLATE,
        python_version=sys.version,
        working_dir=os.getcwd(),
        aws_region=os.getenv('AWS_REGION', 'Not set'),
        kb_id=os.getenv('KB_ID', 'Not set'),
        port=os.getenv('PORT', 'Not set'),
        form_submitted=form_submitted,
        test_input=test_input
    )

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'Flask app running successfully'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)