
import sqlite3 as sq


def db_start():
    with sq.connect('bd.db') as db:
        cur = db.cursor()

        return cur.execute('CREATE TABLE IF NOT EXISTS users('
                           'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'user_id INTEGER,'
                           'balance INTEGER NOT NULL DEFAULT 0,'
                           'UNIQUE(user_id))')
# def db_channal():
#     with sq.connect('bd.db') as db:
#         cur = db.cursor()
#
#         return cur.execute('CREATE TABLE IF NOT EXISTS channals('
#                            'status INTEGER NOT NULL DEFAULT 1)')
#

def db_admin():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('CREATE TABLE IF NOT EXISTS admins('
                           'all_balance INTEGER DEFAULT 0,'
                           'komsa INTEGER NOT NULL DEFAULT 3,'
                           'subs INTEGER NOT NULL DEFAULT 0,'
                           'buttons INTEGER NOT NULL DEFAULT 0)')

def db_url_ref():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('CREATE TABLE IF NOT EXISTS urls('
                           'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'url TEXT,'
                           'symbol TEXT,'
                           'run INTEGER NOT NULL DEFAULT 0)')

def db_new_buton():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS buttons('
                           'name_but TEXT,'
                           'type TEXT,'
                           'text TEXT,'
                           'file_id TEXT,'
                    'keybord TEXT)')
        try:
            cur.execute('SELECT name_but FROM buttons').fetchone()[0]
        except Exception as e:
            print(e)
            cur.execute('INSERT INTO buttons(name_but, type, text, file_id, keybord) VALUES("tt","tt","tt","tt", "tt")')
            db.commit()

def db_new_buton2():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS buttons2('
                           'name_but TEXT,'
                           'type TEXT,'
                           'text TEXT,'
                           'file_id TEXT,'
                    'keybord TEXT)')
        try:
            cur.execute('SELECT name_but FROM buttons2').fetchone()[0]
        except Exception as e:
            print(e)
            cur.execute('INSERT INTO buttons2(name_but, type, text, file_id, keybord) VALUES("tt","tt","tt","tt", "tt")')
            db.commit()


def add_keybord2(keybord):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE buttons2 SET keybord = ?', (keybord,))

def add_keybord(keybord):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE buttons SET keybord = ?', (keybord,))

def add_text2(name, typ, text, id):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        try:
            return cur.execute('UPDATE buttons2 SET name_but = ?, type = ?, text = ?, file_id = ?',(name, typ, text, id))

        except Exception as e:
            print(e)
            cur.execute('INSERT INTO buttons2(name_but, type, text, file_id, keybord) VALUES("tt","tt","tt","tt", "tt")')
            cur.execute('UPDATE buttons2 SET name_but = ?, type = ?, text = ?, file_id = ?', (name, typ, text, id))
            db.commit()


def select_buton2():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('SELECT type, text, file_id, keybord FROM buttons2').fetchone()




def add_text(name, typ, text, id):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        try:
            return cur.execute('UPDATE buttons SET name_but = ?, type = ?, text = ?, file_id = ?',(name, typ, text, id))

        except Exception as e:
            print(e)
            cur.execute('INSERT INTO buttons(name_but, type, text, file_id, keybord) VALUES("tt","tt","tt","tt", "tt")')
            cur.execute('UPDATE buttons SET name_but = ?, type = ?, text = ?, file_id = ?', (name, typ, text, id))
            db.commit()


def select_buton():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('SELECT type, text, file_id, keybord FROM buttons').fetchone()


#Узнаем статус
def op_chek():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        try:
            return cur.execute('SELECT subs FROM admins').fetchone()[0]
        except TypeError:
            cur.execute('INSERT INTO admins(all_balance,komsa,subs,buttons) VALUES(0,3,0,0)')
            return cur.execute('SELECT subs FROM admins').fetchone()[0]


#Выбираем общие пополнения
def all_balance_chek():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('SELECT all_balance FROM admins').fetchone()[0]

def chek_buttons():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('SELECT buttons FROM admins').fetchone()[0]

#Включить кнопки
def on_buttons():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE admins SET buttons = 1')

#Выключить кнопки
def off_buttons():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE admins SET buttons = 0')


#Включить ОП
def on_subs():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE admins SET subs = 1')

#Выкл ОП
def off_subs():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE admins SET subs = 0')


#Удалить все ссылки
def url_delete():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('DELETE FROM urls')

#Выбираем все ссылки
def url_chek():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('SELECT url, run FROM urls').fetchall()

#Увеличиваем счетчик переходов по рефке
def run_update(symbol):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE urls SET run = run + 1 WHERE symbol = ?', (symbol,))


#Добавляем ссылку реф
def add_url(url, symbol):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('INSERT INTO urls(url, symbol) VALUES(?, ?)', (url, symbol))

def komsa_chek():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('SELECT komsa FROM admins').fetchone()


def komsa_update(komsa):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE admins SET komsa = ?', (komsa,))


def update_status_channal():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE channals SET status = 1')


# Проверка пользователя
def user_exists(user_id):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        result = cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
        return bool(len(result))



#Добавление комсы
def add_komsa():
    with sq.connect('bd.db') as db:
        cur = db.cursor()

        cur.execute('INSERT INTO admins(komsa) VALUES (3)')
        db.commit()


#Добавление пользователя
def add_users(user_id):
    with sq.connect('bd.db') as db:
        cur = db.cursor()

        cur.execute('INSERT INTO users(user_id) VALUES (?)', (user_id,))
        db.commit()

#Собираем всех юзеров
def all_users():
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('SELECT user_id FROM users').fetchall()


#Общие пополнения
def add_all_balances(balance):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE admins SET all_balance = all_balance + ?', (balance,))


#Пополняем баланс
def add_balances(user, balance):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (balance, user))

#Проверка баланса
def chek_balance(user_id):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchall()[0]

#Минус баланс
def minus_balance(user_id, balance):
    with sq.connect('bd.db') as db:
        cur = db.cursor()
        return cur.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (balance, user_id))


def main():
    db_start()


if __name__ == '__main__':
    main()