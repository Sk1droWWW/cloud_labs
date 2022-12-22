from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask by Mykhailo'

app.run(host='213.174.29.225', port=80)