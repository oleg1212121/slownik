from flask import Flask, render_template, url_for, request, abort, redirect

import datetime
import db
import re
import json


ALLOWED_EXTENSIONS = {'txt', 'srt'}
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/test")
def test():
    files = [
        # "1-1000.txt",
        # "1000-2000.txt",
        # "2000-3000.txt",
        # "3000-4000.txt",
        # "4000-5000.txt",
        # "5000-6000.txt",
        # "6000-7000.txt",
        # "7000-8000.txt",
        # "8000-9000.txt",
        # "9000-10000.txt",
        # "10000-11000.txt",
    ]
    res = ''
    # dict = [re.sub(r'[^AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż].+$', '', i[1].strip().lower()) for i in db.get_words(1)]
    rows = db.get_words(1)
    f = open("test.txt", "a", encoding='utf-8')
    for row in rows:
        line = f'{row[1]}|||{row[2]}|||{row[3]}|||{row[4]}|||{row[5]}|||{row[6]}\n'
        f.write(line)
    f.close()
    # rows = set()
    # for file in files:
    #     with open(file, 'r', encoding='utf-8') as fd:
    #         for line in fd:
    #             line = re.sub(r'=[0-9]+', '', line).strip().lower()
    #             if len(line) > 2 and line not in dict:
    #                 rows.add((line,"*","*",3,20000))



    # rows = [len(rows)]
    # rows = sorted(rows)
    # rows = [w[0] for w in db.chiki()]

    # rows = sorted(rows)

    return render_template('test.html', rows=rows)


@app.route("/words")
def words():
    words = db.get_words(1)
    return render_template('words.html', words=words)

@app.route("/training")
def training():

    words = db.get_training()
    return render_template('training.html', words=words, time=datetime.datetime.now())

@app.route("/dictionary")
@app.route("/dictionary/<int:status>")
def dictionary(status):
    if status > 1 and not status:
        status = 1
    words = db.get_dictionary(status)
    return render_template('dictionary.html', status=status, words=words)


@app.route("/dictionary/learn/<int:word>/<int:status>")
def learn_rus_word(word, status):
    db.learn_rus_word(word, status, datetime.datetime.now() )
    return 'True'


@app.route("/dictionary/delete/<int:word>")
def delete_rus_word(word):
    db.delete_rus_word(word)
    return 'True'


@app.route("/dictionary/change/<int:word>", methods=['POST'])
def change_rus_word(word):
    db.change_rus_word(word, request.form['word'].strip(), request.form['translate'].strip(), request.form['hint'].strip())
    return 'True'


@app.route("/upload_subtitles")
def upload_subtitles():
    return render_template('upload_subtitles.html')


# @app.route("/series")
# def series():
#     films = db.get_films()
#     return render_template('series.html', films=films)


# @app.route("/series/<int:identifier>")
# def current(identifier):
#     film = db.get_film(identifier)
#     words = db.get_words_by_film(identifier)
#     return render_template('current.html', film=film, words=words)


# @app.route("/known/<int:film>/<int:word>")
# def known(film, word):
#     db.learn_word(word)
#     return 'True'


# @app.route("/add_words", methods=['POST'])
# def add_words():
#     if 'file' not in request.files:
#         return render_template('index.html')
#     file = request.files['file']
#     file.seek(0)
#     content = file.read()
#     content = str(content, 'utf-8')
#     content = re.sub(r'[^A-z\s\']', ' ', content).lower()
#     content = content.replace('[br]', ' ')
#     content = content.replace('[prg]', ' ')
#     content = content.replace('[size]', ' ')
#     content = content.replace('[delay]', ' ')
#     content = content.replace('[filepath]', ' ')
#     content = content.replace('[author]', ' ')
#     content = content.replace('[subtitle]', ' ')
#     content = content.replace('[font]', ' ')
#     content = content.replace('[end]', ' ')
#     content = content.replace('[colf]', ' ')
#     content = content.replace('[information]', ' ')
#     content = content.replace('[style]', ' ')
#     content = content.replace('[source]', ' ')
#     content = content.replace('[comment]', ' ')
#     content = content.replace('[title]', ' ')
#     content = content.replace('[end', ' ')
#     content = content.replace('[cd', ' ')
#     content = content.replace('track]', ' ')
#     content = content.replace('information]', ' ')
#
#     sett = {x for x in content.split()}
#     arr = [(x, 0, 1) for x in sett]
#     current_film = db.create_or_update_film(request.form['title'], arr)
#     return redirect(url_for('current', identifier=current_film))
    # ('current.html', film=current_film[0], words=current_film[1])


@app.route("/info")
def info():
    data = db.get_info()
    stat = {
        9 : 0,
        8 : 0,
        7 : 0,
        6 : 0,
        5 : 0,
        4 : 0,
        3 : 0,
        2 : 0,
        1 : 0,
        0 : 0
    }
    for x in data:
        stat[x[0] if x[0] < 9 else 9] += x[1]
    return render_template('statistic.html', stat=stat)


if __name__ == '__main__':
    db.init_db(refresh=False)
    app.run(debug=True)
