import psycopg2 as cop
import datetime

con = cop.connect(host="localhost", database="backlog", user="postgres", password="postgres")

print("DB connected!")

cur = con.cursor()

def add_rec(title, by, to, platform, year = 0, genre = '', length = '', author = ''):
    dt = datetime.datetime.now()
    cur.execute("INSERT INTO media (title, author, platform, year, genre, length, rec_by, rec_to, created_on, consumed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (title, author, platform, year, genre, length, by, to, f"{dt.date()} {dt.time()}", False))
    con.commit()

    return 0

def get_recs(name, platform = ''):
    if platform == '':
        # SELECT * FROM media WHERE rec_to IN (SELECT alias from user where name in (select name from users where alias = 'Eat The Rich')
        cur.execute("SELECT title, platform, rec_by FROM media WHERE rec_to IN (SELECT alias from users where name in (select name from users where alias = '{0}'));".format(name))
    else:
        cur.execute("SELECT title, platform, rec_by FROM media WHERE rec_to IN (SELECT alias FROM users WHERE name IN (SELECT name FROM users WHERE alias = '{0}')) AND platform = '{1}';".format(name, platform))
    recs = cur.fetchall()
    return recs

def add_alias(name, alias):
    cur.execute("SELECT name, alias FROM users WHERE name = '{0}' AND alias = '{1}'".format(name, alias))
    check = cur.fetchall()
    print(check)
    if len(check) == 0:
        cur.execute("INSERT INTO users (name, alias) VALUES ('{0}', '{1}')".format(name, alias))
        con.commit()
    else:
        return 1
#add_rec('Mulan', 'Cody', 'Levi', 'movie')
#print(get_recs('Levi', 'movie'))