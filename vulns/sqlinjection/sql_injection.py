from flask import render_template


def sql_injection_page(request, app):
    search = request.args.get('search')
    sql = f"SELECT * FROM products WHERE name LIKE '%{search}%'"
    products = app.db_helper.execute_read(sql)

    products = list(
        map(
            lambda p: {
                'id': p[0],
                'name': p[1],
                'price': p[2]
            }, 
            products
        )
    )

    return render_template(
        'sql-injection.html',
        sql=sql,
        products=products,
        search=search
    )


def sql_injection_api(request):
    term = request.args.get('search')

    products = search_products(term)

    return products
