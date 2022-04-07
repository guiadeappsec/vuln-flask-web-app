from flask import render_template


def sql_injection_search_page(request, app):
    search = request.args.get('q')

    sql = f"SELECT * FROM products WHERE name LIKE '%{search}%'"

    db_result = app.db_helper.execute_read(sql)

    products = list(
        map(
            lambda p: {
                'id': p[0],
                'name': p[1],
                'price': p[2]
            },
            db_result
        )
    )

    return render_template(
        'sql_injection/search.html',
        sql=sql,
        products=products
    )
