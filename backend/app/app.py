from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
# from flask_login import LoginManager
# # from models import db, User
from api.users import user_routes
from api.webhook import webhook_routes
from api.auctions import auction_routes
from api.auth import auth_routes
from api.nfts import nft_routes
from auction_utils import confirm_new_bid
# from config import Config
from flask_socketio import SocketIO
app = Flask(__name__)

# # Setup login manager
# login = LoginManager(app)
# login.login_view = 'auth.unauthorized'

# app.config.from_object(Config)
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
socketio = SocketIO(app)

app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(webhook_routes, url_prefix='/webhook')
app.register_blueprint(nft_routes, url_prefix='/nft')
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(auction_routes, url_prefix='/auction')
# db.init_app(app)

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
def send_socket_message(event_name, data):
    socketio.emit(event_name, data)


#     return response
if __name__ == '__main__':
    app.run()
    socketio.run(app)
