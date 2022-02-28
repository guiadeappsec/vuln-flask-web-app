


from flask import render_template, send_file


def path_traversal_page(request, app):
    return render_template("path-traversal.html")


def path_traversal_image(request, app):
    image_path = f"{app.config['PUBLIC_IMG_FOLDER']}/{request.args.get('img')}"

    return send_file(image_path)