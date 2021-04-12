import site
# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/FlaskApp/FlaskApp/venv/lib/python3.8/site-packages')
from flask_socketio import SocketIO, emit, disconnect
# http://brunorocha.org/python/flask/using-flask-cache.html
# from flask_caching import Cache
from flask import Flask, render_template, request, session
import random
import yaml
import logging
import sys


logging.basicConfig(stream=sys.stderr)
# logging.basicConfig(filename='/var/log/apache2/record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


config = {
    "DEBUG": True,          # some Flask specific configs
    # "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    # "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    # "CACHE_DIR": "/var/tmp",
    # "CACHE_DEFAULT_TIMEOUT": 7200,
    "SECRET_KEY": "fsdfsd_adasd"
}

async_mode = None
app = Flask(__name__)
# socket_ = SocketIO(app, async_mode=async_mode)

# Instantiate the cache
# cache = Cache()
# cache.init_app(app=app, config={"CACHE_TYPE": "SimpleCache"})

# tell Flask to use the above defined config
app.config.from_mapping(config)
# cache = Cache(app)


@app.route("/", methods=['GET', 'POST'])
# @cache.cached(timeout=3600)
def index():
    idx, w = get_word(get_ordabok())
    # cache.set("wordidx"+get_unique_session_id(), idx)
    # app.logger.debug("caching wordidx"+get_unique_session_id())
    session['word_index']=idx
    app.logger.debug("session variable word_index set to " + str(idx))
    #for env_var in request.environ:
    #  app.logger.debug(env_var + ": " )
    return render_template('index.html', wort=w['de'])


@app.route('/lausn', methods=['POST'])
def show_solution():
    # idx = cache.get("wordidx"+get_unique_session_id())
    idx=session['word_index']
    # app.logger.debug("getting cached wordidx"+get_unique_session_id())
    # app.logger.debug("word indx {0}".format(idx))
    w = get_word_by_index(get_ordabok(), int(idx))
    if not w:
        app.logger.error("cache empty? Got no index")
        index()
    if w['class']=='nafnorð':
        result_w = w['is'] + " (" + w['kyns'] + ")"
        result_as = str(w['arnastofnun'])
        beyging_nf = w['beyging']['nf']
        beyging_pf = w['beyging']['pf']
        app.logger.debug("Beyging Nf. eintala = {0}".format(beyging_nf[0]))
        return render_template('lausn_nafnord.html', wort=result_w,
                                arnastofnun=result_as,
                                nf1=beyging_nf[0], nf2=beyging_nf[1],
                                nf3=beyging_nf[2], nf4=beyging_nf[3],
                                pf1=beyging_pf[0], pf2=beyging_pf[1],
                                pf3=beyging_pf[2], pf4=beyging_pf[3])
    elif w['class'] == 'sagnorð':
        result_w = w['is'] + " (" + w['sagnorð-class'] + "-Klasse)"
        result_as = str(w['arnastofnun'])
        beyging_fn = w['Framsöguháttur']['Nútíð']
        beyging_fp = w['Framsöguháttur']['Þátíð']
        # app.logger.debug("Beyging Nf. eintala = {0}".format(beyging_fn[0]))
        return render_template('lausn_sagnord.html', wort=result_w,
                               arnastofnun=result_as,
                               fn1=beyging_fn[0], fn2=beyging_fn[1],
                               fn3=beyging_fn[2], fn4=beyging_fn[3],
                               fn5=beyging_fn[4], fn6=beyging_fn[5],
                               fp1=beyging_fp[0], fp2=beyging_fp[1],
                               fp3=beyging_fp[2], fp4=beyging_fp[3],
                               fp5=beyging_fp[4], fp6=beyging_fp[5])
    else:
        index()



# def get_unique_session_id():
#     client_ip = request.environ.get('REMOTE_ADDR')
#     return client_ip.replace('.', '')


def get_ordabok():
    with open('/var/www/FlaskApp/FlaskApp/etc/ordabok2.yaml', 'rt', encoding='utf') as f:
        return yaml.safe_load(f.read())


def get_word(words):
    idx = random.randint(0, len(words)-1)
    return idx, words[idx]


def get_word_by_index(words, idx):
    return words[idx]


if __name__ == "__main__":
    app.run()
    # socket_.run(app, debug=True)
