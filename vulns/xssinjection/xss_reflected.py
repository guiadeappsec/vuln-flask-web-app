from flask import render_template


def xss_reflected_page(request):
    return render_template('xss-reflected.html')
