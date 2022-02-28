from flask import render_template


def xss_stored_page(request, app):
    messages = app.db_helper.execute_read('SELECT * FROM messages', {})
    messages = list(map(lambda it: it[0], messages))

    return render_template('xss-stored.html', messages=messages)


def xss_stored_api(request, app):
    message = request.form['message']
    result = app.db_helper.execute_write('INSERT INTO messages (message) VALUES (:msg)', { 'msg': message })

    return xss_stored_page(request, app)