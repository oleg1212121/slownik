import sqlite3

def init_db(refresh: bool = False):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        if refresh:
            cursor.execute('DROP TABLE IF EXISTS words')

        cursor.execute("""CREATE TABLE IF NOT EXISTS words (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            word text UNIQUE,
                            translate text,
                            is_known INTEGER,
                            frequency INTEGER,
                            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            hint text
                            )""")

        if refresh:
            words = set()
            with open("dictionary.txt", "r", encoding="utf8") as file1:
                counter = 1
                for line in file1.readlines():
                    line = line.split('|')
                    item = (line[1].strip(), line[2].strip() or "", 0, line[3].strip() or 0)
                    words.add(item)
                    counter = counter + 1
            cursor.executemany(f"""INSERT INTO words (word, translate, is_known, frequency) VALUES (?,?,?,?) ON CONFLICT(word) DO UPDATE SET translate = excluded.translate, frequency = excluded.frequency""", words)
        connection.commit()



def get_training():
    res = []
    UK = 1
    FK = 0.1
    IK = 1
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT *, (strftime('%s', DATE('now','+2 day')) - strftime('%s', updated_at))/3600 as gg
            FROM words  ORDER BY (
            ((strftime('%s', DATE('now','+2 day')) - strftime('%s', updated_at)) * {UK} +
            (frequency * {FK})) /
            (is_known * is_known * {IK} + 1)
            ) DESC 
            limit 200""")
            res = cursor.fetchall()
    except:
        pass
    return res

def get_dictionary(status):
    res = []
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM words WHERE is_known = {status} ORDER BY updated_at, frequency DESC limit 200""")
            res = cursor.fetchall()
    except:
        pass
    return res


def learn_rus_word(word, status, t):
    res = False
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""UPDATE words SET is_known = {status}, updated_at = '{t}' WHERE id = {word}""")
            connection.commit()
            res = True
    except:
        pass
    return res


def change_rus_word(identifier, word, translate, hint):
    res = False
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""UPDATE words SET word = ?, translate = ?, hint = ? WHERE id = {identifier}""",
                           (word, translate, hint))
            connection.commit()
            res = True
    except:
        pass
    return res


def delete_rus_word(word):
    res = False
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""DELETE FROM words WHERE id = {word}""")
            connection.commit()
            res = True
    except:
        pass
    return res


def get_word(identifier):
    res = None
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM words WHERE id = {identifier} LIMIT 1""")
            res = cursor.fetchone()
    except:
        pass
    return res


def get_words(flag):
    res = []
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM words""")
            res = cursor.fetchall()
    except:
        pass
    return res



# def get_film(identifier=None):
#     res = None
#     try:
#         with sqlite3.connect("database.db") as connection:
#             cursor = connection.cursor()
#             if identifier:
#                 cursor.execute(f"""SELECT * FROM films WHERE id = {identifier} LIMIT 1""")
#             else:
#                 cursor.execute(f"""SELECT * FROM films WHERE rowid = last_insert_rowid() LIMIT 1""")
#             res = cursor.fetchone()
#     except:
#         pass
#     return res


# def get_words_by_film(identifier):
#     res = []
#     try:
#         with sqlite3.connect("database.db") as connection:
#             cursor = connection.cursor()
#             cursor.execute(f"""SELECT * FROM words LEFT JOIN word_film ON word_film.word_id = words.id
#                                 WHERE word_film.film_id = {identifier} AND words.is_known = 0""")
#             res = cursor.fetchall()
#     except:
#         pass
#     return res


def create_or_update_words(items):
    res = False
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.executemany(f"""INSERT INTO words (word, is_known, is_sync) VALUES (?,?,?)
                                ON CONFLICT(word) DO UPDATE SET is_sync = excluded.is_sync""", items)
            connection.commit()
            res = True
    except:
        pass
    return res


# def create_or_update_film(film, words):
#     res = False
#     try:
#         with sqlite3.connect("database.db") as connection:
#             cursor = connection.cursor()
#             cursor.execute(f"""INSERT INTO films (title) VALUES ('{film}')""")
#             res = cursor.lastrowid
#             cursor.executemany(f"""INSERT INTO words (word, is_known, is_sync) VALUES (?,?,?)
#                                     ON CONFLICT(word) DO UPDATE SET is_sync = 1""", words)
#             cursor.execute(f"""SELECT * FROM words WHERE is_sync = 1""")
#             words = cursor.fetchall()
#             syncs = [(i[0], res) for i in words]
#             cursor.executemany(f"""INSERT INTO word_film (word_id, film_id) VALUES (?,?)""", syncs)
#             cursor.execute(f"""UPDATE words SET is_sync = 0 WHERE is_sync = 1""")
#             connection.commit()
#     except:
#         pass
#     return res


def learn_word(word):
    res = False
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""UPDATE words SET is_known = 1 WHERE id = {word}""")
            connection.commit()
            res = True
    except:
        pass
    return res


# def get_films():
#     res = []
#     try:
#         with sqlite3.connect("database.db") as connection:
#             cursor = connection.cursor()
#             cursor.execute(f"""SELECT * FROM films""")
#             res = cursor.fetchall()
#     except:
#         pass
#     return res


def get_info():
    res = []
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT is_known, count(*) FROM words GROUP BY is_known ORDER BY is_known DESC""")
            res = cursor.fetchall()
    except:
        pass
    return res


def up():

    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""UPDATE words SET is_known = 4 WHERE frequency = 80000""")
            connection.commit()
            res = True
    except:
        pass
    return res


def lalala(items):
    res = False
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.executemany(f"""INSERT INTO words (word, translate, hint, is_known, frequency) VALUES (?,?,?,?,?)
                                ON CONFLICT(word) DO NOTHING""", items)
            connection.commit()
            res = True
    except:
        pass
    return res

def chiki():
    res = []
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT word FROM words WHERE frequency=20000 AND translate='*'""")
            res = cursor.fetchall()
    except:
        pass
    return res

def puki(items):
    res = False
    try:
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.executemany(f"""INSERT INTO words (word, translate) VALUES (?,?)
                                ON CONFLICT(word) DO UPDATE SET translate = excluded.translate""", items)
            connection.commit()
            res = True
    except:
        pass
    return res
