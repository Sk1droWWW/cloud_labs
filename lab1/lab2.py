from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask by Mykhailo'

app.run(host='15.188.65.11', port=81)