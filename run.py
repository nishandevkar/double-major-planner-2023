from app import app
from flask import Flask, render_template
import os

app.jinja_env.globals.update(enumerate=enumerate)

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)  # Use 5000 as a default port if PORT is not set
    app.run(host='0.0.0.0', port=port)



