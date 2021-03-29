# Add the site-packages of the chosen virtualenv to work with
import random
import yaml
from flask import Flask, render_template
import site
site.addsitedir('/var/www/FlaskApp/FlaskApp/venv/lib/python3.8/site-packages')

app = Flask(__name__)


class wordbook:
    def __init__(self, words):
        self.words = words
        self.wordidx, self.word = self.get_next_word()

    def get_next_word(self):
        idx = random.randint(0, len(self.words)-1)
        return idx, self.words[idx]

    def get_word(self):
        return self.word

    def get_word_by_index(self, idx):
        return self.words[idx]


@app.route("/", methods=['GET', 'POST'])
def index():
    # w = get_word(get_ordabok())
    w = wb.get_word()
    # return "Lææa islensku"
    return render_template('index.html', wort=w['de'])


def get_ordabok():
    with open('/var/www/FlaskApp/FlaskApp/etc/ordabok2.yaml', 'rt', encoding='utf') as f:
        return yaml.safe_load(f.read())


def get_word(words):
    idx = random.randint(0, len(words)-1)
    return words[idx]


@app.route('/lausn', methods=['POST'])
def show_solution():
    w = get_word(get_ordabok())
    return render_template('lausn.html', wort=w['is'])


if __name__ == "__main__":
    wb = wordbook(get_ordabok())
    app.run()
