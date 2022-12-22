from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask by Mykhailo'

app.run(host='69.214.126.103', port=81)