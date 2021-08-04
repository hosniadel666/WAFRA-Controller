import sqlite3
import cgi

PATH_2_DB = '/home/pi/Desktop/cvs_internship/web_app/cvs.db'

def application(env, start_line):
    
    if env['REQUEST_METHOD'] == 'POST':   ## add new DB record
        return handle_post(env, start_line)
    elif env['REQUEST_METHOD'] == 'GET':  ## create HTML-fragment report
        return handle_get(start_line)
    else:                                 ## no other option for now
        start_line('405 METHOD NOT ALLOWED', [('Content-Type', 'text/plain')])
        response_body = 'Only POST and GET verbs supported.'
        return [response_body.encode()]


def handle_post(env, start_line):
    form = get_field_storage(env)  ## body of an HTTP POST request
    ## Extract fields from POST form.
    num = form.getvalue('num')
    dis = form.getvalue('discription')
    isdigital = form.getvalue('isdigital')
    data = form.getvalue('data')

    ## Missing info?
    if (num is not None and dis is not None and isdigital is not None and data is not None):
        add_record(num, dis, isdigital, data)
        response_body = "POST request handled.\n"
        start_line('201 OK', [('Content-Type', 'text/plain')])
    else:
        response_body = "Missing info in POST request.\n"
        start_line('400 Bad Request', [('Content-Type', 'text/plain')])

    return [response_body.encode()]

def handle_get(start_line):
    conn = sqlite3.connect(PATH_2_DB)        ## connect to DB
    cursor = conn.cursor()                   ## get a cursor
    cursor.execute("select * from sensors")

    response_body = "<h3>Sensors report</h3><ul>"
    rows = cursor.fetchall()
    for row in rows:
	
        response_body += "<li>" + "id : " + str(row[0]) + "</li>" + "\n"
	response_body += "<li>" + "sensor num : " + str(row[1]) + "</li>" + "\n"
        response_body += "<li>" + "sensor discription : " + str(row[2]) + "</li>" + "\n"
	response_body += "<li>" + "is it digital : " + str(row[3]) + "</li>" + "\n"
	response_body += "<li>" + "reading : " + str(row[4]) +  "</li>" + "\n"
	response_body += "<br>"

    response_body += "</ul>"

    conn.commit()  ## commit
    conn.close()   ## cleanup
   
    start_line('200 OK', [('Content-Type', 'text/html')])
    return [response_body.encode()]

## Add a record from a device to the DB.
def add_record(num, discription, isdigital, data):
    conn = sqlite3.connect(PATH_2_DB)      ## connect to DB
    cursor = conn.cursor()                 ## get a cursor

    sql = "INSERT INTO sensors (num, discription, isdigital, data) values (?,?,?,?)"
    cursor.execute(sql, (num, discription, isdigital, data)) ## execute INSERT

    conn.commit()  ## commit
    conn.close()   ## cleanup

def get_field_storage(env):
    input = env['wsgi.input']
    form = env.get('wsgi.post_form')
    if (form is not None and form[0] is input):
        return form[2]
    fs = cgi.FieldStorage(fp = input, environ = env, keep_blank_values = 1)
    return fs
