import os
from flask import Flask, render_template, request, redirect, send_from_directory
# from flask_cors import CORS
# from flask_wtf.csrf import CSRFProtect, generate_csrf
# from flask_login import LoginManager
from models import db, User
from api.users import user_routes
from api.webhook import webhook_routes


app = Flask(__name__)

# # Setup login manager
# login = LoginManager(app)
# login.login_view = 'auth.unauthorized'


# @app.route('/')
# def serve():
#     return render_template("index.html")


# @app.route('/<path:path>')
# def catch_all(path):
#     return send_from_directory("../frontend/build/", path)

# CORS(app)


# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(webhook_routes, url_prefix='/webhook')
db.init_app(app)

# Application Security
# CORS(app)

# Since we are deploying with Docker and Flask,
# we won't be using a buildpack when we deploy to Heroku.
# Therefore, we need to make sure that in production any
# request made over http is redirected to https.
# Well.........


# @app.before_request
# def https_redirect():
#     if os.environ.get('FLASK_ENV') == 'production':
#         if request.headers.get('X-Forwarded-Proto') == 'http':
#             url = request.url.replace('http://', 'https://', 1)
#             code = 301
#             return redirect(url, code=code)


# @app.after_request
# def inject_csrf_token(response):
#     response.set_cookie('csrf_token',
#                         generate_csrf(),
#                         secure=True if os.environ.get(
#                             'FLASK_ENV') == 'production' else False,
#                         samesite='Strict' if os.environ.get(
#                             'FLASK_ENV') == 'production' else None,
#                         httponly=True)
#     return response

