from flask import Blueprint, render_template

start = Blueprint('start', __name__)

@start.route('/', methods=['GET'])
def main():
    return render_template("index.html")
    
