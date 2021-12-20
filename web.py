from flask import Flask, render_template, redirect, url_for, request
import psycopg2
import sys

from datetime import datetime



app = Flask(__name__)


@app.route('/', methods = ['GET'])

def hello_world():
    print('Hello_world')
    return render_template('index.html')


################## TAGS BEGIN

@app.route('/add_tag', methods=['POST'])

def add_tag():
    # curl -i -H "Content-Type: application/json" -X POST -d '{"name": "math"}' http://localhost:5000/add_tag

    name = request.json['name']
    print(name)

    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        cur = con.cursor()

        sql = """INSERT INTO "Logic".tags(name)
                VALUES(%s) RETURNING id;"""

        cur.execute(sql, (name,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        print(vendor_id)
        # commit the changes to the database
        con.commit()

        # version = cur.fetchone()[0]
        # print(version)

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    return 'OK'

@app.route('/get_tags', methods=['GET'])

def get_tags():
    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        
        cur = con.cursor()
        cur.execute('SELECT * FROM "Logic".tags')

        columns = [column[0] for column in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        # rows = cur.fetchall()
        # for row in rows:
        #     print(f"{row[0]} {row[1]}")
       

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    print(results)

    return {"result": results}


def get_tag_id_by_name(name):
    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        
        cur = con.cursor()
        sql = """SELECT id FROM "Logic".tags WHERE "Logic".tags.name = '{}';""".format(name)

        cur.execute(sql)
        id = cur.fetchone()[0]
        print(type(id))

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()


    return str(id)


################## TAGS FINISH

@app.route('/add_board', methods=['POST'])

def add_board():

     # curl -i -H "Content-Type: application/json" -X POST -d '{"name": "math memes", "tag_name":"memes"}' http://localhost:5000/add_board

    name = request.json['name']
    tag_name = request.json['tag_name']
    print(name, tag_name)

    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        cur = con.cursor()

        sql = """INSERT INTO "Logic".boards(name, tag_id)
                VALUES('{}', {}) RETURNING id;""".format(name, get_tag_id_by_name(tag_name))

        print(sql)

        cur.execute(sql)
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        print(vendor_id)
        # commit the changes to the database
        con.commit()

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    return 'OK'


@app.route('/get_boards', methods=['GET'])

def get_boards():
    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        
        cur = con.cursor()
        cur.execute('SELECT * FROM "Logic".boards')

        columns = [column[0] for column in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        # rows = cur.fetchall()
        # for row in rows:
        #     print(f"{row[0]} {row[1]}")
       

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    print(results)

    return {"result": results}


def get_board_id_by_name(name):

    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        
        cur = con.cursor()
        sql = """SELECT id FROM "Logic".boards WHERE "Logic".boards.name = '{}';""".format(name)

        cur.execute(sql)
        id = cur.fetchone()[0]
        print(type(id))

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()


    return str(id)

@app.route('/get_threads', methods=['GET'])

def get_threads_by_board():

     # curl -i -H "Content-Type: application/json" -X GET -d '{"board_name": "b"}' http://localhost:5000/get_threads

    board_name = request.json['board_name']
    board_id = get_board_id_by_name(board_name)

    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        
        cur = con.cursor()
        sql = """SELECT * FROM "Logic".threads WHERE "Logic".threads.board_id = '{}';""".format(board_id)

        cur.execute(sql)

        columns = [column[0] for column in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        # rows = cur.fetchall()
        # for row in rows:
        #     print(f"{row[0]} {row[1]}")
       

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    print(results)

    return {"result": results}


@app.route('/create_thread', methods=['POST'])

def create_thread():


     # curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Hello wrold, ето мой первый тред", "image": "https://kartinki-dlya-srisovki.ru/wp-content/uploads/2018/11/gubka-bob-1.jpg", "tag_name":"fun", "board_name":"b", "user_id" : 1}' http://localhost:5000/create_thread

    name = request.json['name']
    image = request.json['image']
    tag_name = request.json['tag_name']

    board_name = request.json['board_name']
    board_id = get_board_id_by_name(board_name)

    tag_id = get_tag_id_by_name(tag_name)

    creator = request.json['user_id']

    time_of_create = datetime.now()

    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        cur = con.cursor()

        sql = """INSERT INTO "Logic".threads(time_of_create, name, image, board_id, tag_id, creator_id)
                VALUES('{}', '{}', '{}', {}, {}, {}) RETURNING id;""".format(time_of_create, name, image, board_id, tag_id, 1)

        print(sql)

        cur.execute(sql)
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        print(vendor_id)
        # commit the changes to the database
        con.commit()

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    return 'OK'



@app.route('/add_reply', methods=['POST'])

def add_reply():

    #curl -i -H "Content-Type: application/json" -X POST -d '{"text": "Its first comment", "tag_name": "chill", "replied_id": "None", "commentator_id": 1, "thread_id" : 2}' http://localhost:5000/add_reply
    text = request.json['text']
    print(text)
    tag_name = request.json['tag_name']
    tag_id = get_tag_id_by_name(tag_name)

    replied_id = request.json['replied_id']
    commentator_id = request.json['commentator_id']
    thread_id = request.json['thread_id']

    print(replied_id)

    

    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        cur = con.cursor()

        if replied_id == "None":

            sql = """INSERT INTO "Logic".replies(text, tag_id, replied_id, commentator_id, thread_id)
                    VALUES('{}', {}, NULL, {}, {}) RETURNING id;""".format(text, tag_id, commentator_id, thread_id)
            
        else:

            sql = """INSERT INTO "Logic".replies(text, tag_id, replied_id, commentator_id, thread_id)
                    VALUES('{}', {}, {}, {}, {}) RETURNING id;""".format(text, tag_id, replied_id, commentator_id, thread_id)

        print(sql)

        cur.execute(sql)
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        print(vendor_id)
        # commit the changes to the database
        con.commit()

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    return 'OK'

@app.route('/get_replies', methods=['GET'])

def get_replies():

     # curl -i -H "Content-Type: application/json" -X GET -d '{"thread_id": 2}' http://localhost:5000/get_replies

    thread_id = request.json['thread_id']

    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')

        print(thread_id)

        
        cur = con.cursor()
        sql = """SELECT * FROM "Logic".replies WHERE "Logic".replies.thread_id = {};""".format(thread_id)

        cur.execute(sql)

        columns = [column[0] for column in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        # rows = cur.fetchall()
        # for row in rows:
        #     print(f"{row[0]} {row[1]}")
       

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    print(results)

    return {"result": results}


@app.route('/get_by_tag', methods=['GET'])

def get_by_tag():

     # curl -i -H "Content-Type: application/json" -X GET -d '{"tag_name": "chill"}' http://localhost:5000/get_by_tag

    tag_name = request.json['tag_name']
    tag_id = get_tag_id_by_name(tag_name)

    con = None
    try:

        con = psycopg2.connect(database='db_test', user='u_test',
                            port=1984,
                            host="92.242.58.173",
                            password='testpwd')


        
        cur = con.cursor()
        sql = """SELECT * FROM "Logic".replies WHERE "Logic".replies.tag_id = {};""".format(tag_id)

        cur.execute(sql)

        columns = [column[0] for column in cur.description]
        replies = []
        for row in cur.fetchall():
            replies.append(dict(zip(columns, row)))

        
        sql = """SELECT * FROM "Logic".boards WHERE "Logic".boards.tag_id = {};""".format(tag_id)

        cur.execute(sql)

        columns = [column[0] for column in cur.description]
        boards = []
        for row in cur.fetchall():
            boards.append(dict(zip(columns, row)))

        sql = """SELECT * FROM "Logic".threads WHERE "Logic".threads.tag_id = {};""".format(tag_id)

        cur.execute(sql)

        columns = [column[0] for column in cur.description]
        threads = []
        for row in cur.fetchall():
            threads.append(dict(zip(columns, row)))

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    
    finally:
        if con:
            con.close()

    return {"replies": replies, "boards": boards, "threads" : threads}


