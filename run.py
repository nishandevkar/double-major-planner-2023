from app import app
from flask import Flask, render_template

app.jinja_env.globals.update(enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)
