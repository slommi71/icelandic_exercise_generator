# Add the site-packages of the chosen virtualenv to work with
import random
import yaml
import site
site.addsitedir('/var/www/FlaskApp/FlaskApp/venv/lib/python3.8/site-packages')
from flask import Flask, render_template
from common import cache


app = Flask(__name__)
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Path('/tmp')})


# class wordbook:
#     def __init__(self, words):
#         self.words = words
#         self.wordidx, self.word = self.get_next_word()

#     def get_next_word(self):
#         idx = random.randint(0, len(self.words)-1)
#         return idx, self.words[idx]

#     def get_word(self):
#         return self.word

#     def get_word_by_index(self, idx):
#         return self.words[idx]


@app.route("/", methods=['GET', 'POST'])
def index():
    #w = wb.get_word()
    idx, w = get_word(get_ordabok())
    cache.set("wordidx", idx)
    # return "Lææa islensku"
    return render_template('index.html', wort=w['de'])


def get_ordabok():
    with open('/var/www/FlaskApp/FlaskApp/etc/ordabok2.yaml', 'rt', encoding='utf') as f:
        return yaml.safe_load(f.read())


def get_word(words):
    idx = random.randint(0, len(words)-1)
    return idx, words[idx]

def get_word_by_index(words, idx):
    idx = random.randint(0, len(words)-1)
    return idx, words[idx]

@app.route('/lausn', methods=['POST'])
def show_solution():
    w = get_word_by_index(get_ordabok(), cache.get("wordidx"))
    return render_template('lausn.html', wort=w['is'])


if __name__ == "__main__":
    # wb = wordbook(get_ordabok())
    app.run()
