# Add the site-packages of the chosen virtualenv to work with
import site
site.addsitedir('/var/www/FlaskApp/FlaskApp/venv/lib/python3.8/site-packages')
from flask import Flask, render_template
import yaml
import random

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    w = get_word(get_ordabok())
    #return "Lææa islensku"
    return render_template('index.html', wort=w['de'])

def get_ordabok():
  with open('/var/www/FlaskApp/FlaskApp/etc/ordabok2.yaml', 'rt', encoding='utf') as f:
        return yaml.safe_load(f.read())

def get_word(words):
   idx = random.randint(0,len(words)-1)
   return words[idx]

@app.route('/lausn', methods=['POST'])
def show_solution():
    w=get_word(get_ordabok())
    return render_template('lausn.html', wort=w['is'])


if __name__ == "__main__":
    app.run()