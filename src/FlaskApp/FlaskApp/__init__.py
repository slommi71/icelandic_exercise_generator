import random
import yaml
import site
import logging
import sys

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/FlaskApp/FlaskApp/venv/lib/python3.8/site-packages')
from flask_caching import Cache
from flask import Flask, render_template

logging.basicConfig(stream=sys.stderr)
# logging.basicConfig(filename='/var/log/apache2/record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


config = {
    "DEBUG": True,          # some Flask specific configs
    # "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DIR": "/var/tmp",
    "CACHE_DEFAULT_TIMEOUT": 7200
}
app = Flask(__name__)

# Instantiate the cache
# cache = Cache()
# cache.init_app(app=app, config={"CACHE_TYPE": "SimpleCache"})

# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)


@app.route("/", methods=['GET', 'POST'])
# @cache.cached(timeout=3600)
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
    app.logger.debug("indx {0}".format(idx))
    w = get_word_by_index(get_ordabok(), int(idx))
    if not w:
        app.logger.error("cache empty? Got no indexyy")
        index()
    result_w = w['is'] + " (" + w['kyns'] + ")"
    result_as = str(w['arnastofnun'])
    beyging_nf = nf1=w['beyging']['nf']
    beyging_pf = nf1=w['beyging']['pf']
    app.logger.debug("Beyging Nf. eintala = {0}".format(beyging_nf[0]))
    return render_template('lausn.html', wort=result_w, arnastofnun=result_as,nf1=beyging_nf[0], nf2=beyging_nf[1], nf3=beyging_nf[2], nf4=beyging_nf[3], pf1=beyging_pf[0], pf2=beyging_pf[1], pf3=beyging_pf[2], pf4=beyging_pf[3])
    #return render_template('lausn.html', wort="str(idx)")


if __name__ == "__main__":
    app.run()
