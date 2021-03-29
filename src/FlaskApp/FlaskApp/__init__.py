import random
import yaml
import site
#import logging

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/FlaskApp/FlaskApp/venv/lib/python3.8/site-packages')
from flask_caching import Cache
from flask import Flask, render_template


app = Flask(__name__)

# Instantiate the cache
cache = Cache()
cache.init_app(app=app, config={"CACHE_TYPE": "SimpleCache"})


@app.route("/", methods=['GET', 'POST'])
def index():
    idx, w = get_word(get_ordabok())
    cache.set("wordidx", idx)
    #return render_template('index.html', wort=str(idx))
    return render_template('index.html', wort=w['de'])


def get_ordabok():
    with open('/var/www/FlaskApp/FlaskApp/etc/ordabok2.yaml', 'rt', encoding='utf') as f:
        return yaml.safe_load(f.read())


def get_word(words):
    idx = random.randint(0, len(words)-1)
    return idx, words[idx]


def get_word_by_index(words, idx):
    return words[idx]


@app.route('/lausn', methods=['POST'])
def show_solution():
    idx = cache.get("wordidx")
    #logging.debug("indx {0}".format(idx))
    w = get_word_by_index(get_ordabok(), int(idx))
    result = w['is'] + "(" + w['kyns'] + ")"
    return render_template('lausn.html', wort=result)
    #return render_template('lausn.html', wort="str(idx)")


if __name__ == "__main__":
    app.run(debug=True)
