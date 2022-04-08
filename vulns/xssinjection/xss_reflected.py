from flask import render_template


def xss_reflected_page(request, app):
    search = request.args.get('search')

    products = app.db_helper.execute_read(
        f"SELECT * FROM products WHERE name LIKE :search",
        { 'search': f'%{search}%' }
    )

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
        'xss-reflected.html',
        products=products
    )
