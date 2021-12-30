from urllib import parse
from flask import Blueprint, jsonify, session, request
from app.models import User, db
from app.forms import LoginForm
from app.forms import SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.request import Request, urlopen
from urllib.parse import urlencode, unquote
from json import loads
from os import environ
import http

http.client.HTTPConnection.debuglevel = 1

auth_routes = Blueprint('auth', __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f"{field} : {error}")
    return errorMessages


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        # use this ^ to check session user info
        # by default, current_user is attached everywhere,
        # but value is not None, its some anonymous stuff
        return current_user.to_dict()
    return {'errors': ['Unauthorized']}


@auth_routes.route('/login/', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # print(request.get_json())
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        user = User.query.filter(User.email == form.data['email']).first()
        login_user(user)
        return user.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/logout/', methods=["DELETE"])
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup/', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            first_name=form.data['firstName'],
            last_name=form.data['lastName'],
            email=form.data['email'],
            password=form.data['password'],
            role=form.data["role"]
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return user.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': ['Unauthorized']}, 401

@auth_routes.route("/linkedInSignUp/", methods=["POST"])
def linkedIn_sign_up():
    data = request.json
    token = data["token"]
    redirect_uri = data["redirect_URI"]
    sendoff = {
        "grant_type": "authorization_code",
        "code": token,
        "client_id": environ.get("LINKEDIN_CLIENT_ID"),
        "client_secret": environ.get("LINKEDIN_CLIENT_SECRET"),
        "redirect_uri": redirect_uri
    }
    launch = urlencode(sendoff).encode()
    request_send = Request("https://www.linkedin.com/oauth/v2/accessToken", data=launch)
    response = urlopen(request_send)
    response2 = response.read().decode("utf-8")
    parsed_response = loads(response2)
    # now break down the user info
    access_token = parsed_response["access_token"]
    request_user_info = Request("https://api.linkedin.com/v2/me?projection=(id,firstName,lastName,profilePicture(displayImage~:playableStreams))", headers={"Authorization": f"Bearer {access_token}"})
    # request_user_info = Request("https://api.linkedin.com/v2/me", headers={"Authorization": f"Bearer {access_token}"})
    user_response = urlopen(request_user_info)
    user_response2 = user_response.read().decode("utf-8")
    parsed_response2 = loads(user_response2)
    profilePhoto = parsed_response2["profilePicture"]["displayImage~"]["elements"][0]["identifiers"][0]["identifier"]
    firstName = parsed_response2["firstName"]["localized"]["en_US"]
    lastName = parsed_response2["lastName"]["localized"]["en_US"]
    request_user_info = Request("https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))", headers={"Authorization": f"Bearer {access_token}"})
    user_response3 = urlopen(request_user_info)
    user_response4 = user_response3.read().decode("utf-8")
    parsed_response3 = loads(user_response4)
    email = parsed_response3["elements"][0]["handle~"]["emailAddress"]
    return {"firstName": firstName, "lastName": lastName, "profilePhoto": profilePhoto, "email": email}

@auth_routes.route("/linkedIncreate/", methods=["POST"])
def linkedIn_create_user():
    data = request.json
    print(data, "this is the linkedln debug data")
    user = User.query.filter(User.email == data["email"]).first()
    if user == None:
        package = {
            "first_name": data["firstName"],
            "last_name": data["lastName"],
            "email": data["email"],
            "password": data["password"],
            "role": data["role"],
            "profile_photo": data["profilePhoto"]
        }
        user = User(**package)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return user.to_dict()


@auth_routes.route("/linkedInSignIn/", methods=["POST"])
def linkedIn_sign_in():
    data = request.json
    token = data["token"]
    redirect_uri = data["redirect_URI"]
    sendoff = {
        "grant_type": "authorization_code",
        "code": token,
        "client_id": environ.get("LINKEDIN_CLIENT_ID"),
        "client_secret": environ.get("LINKEDIN_CLIENT_SECRET"),
        "redirect_uri": redirect_uri
    }
    launch = urlencode(sendoff).encode()
    request_send = Request("https://www.linkedin.com/oauth/v2/accessToken", data=launch)
    response = urlopen(request_send)
    response2 = response.read().decode("utf-8")
    parsed_response = loads(response2)
    access_token = parsed_response["access_token"]
    # get email to log in
    request_user_info = Request("https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))", headers={"Authorization": f"Bearer {access_token}"})
    user_response = urlopen(request_user_info)
    user_response2 = user_response.read().decode("utf-8")
    parsed_response2 = loads(user_response2)
    email = parsed_response2["elements"][0]["handle~"]["emailAddress"]
    user = User.query.filter(User.email == email).first()
    if user:
        login_user(user)
        return user.to_dict()
    else:
        return {"errors": ["Cannot find a registered user from the provided LinkedIn credentials"]}, 400

@auth_routes.route("/googleSignUp/", methods=["POST"])
def google_sign_up():
    data = request.json
    token = data["code"]
    redirect_uri = data["redirect_URI"]
    sendoff = {
        "grant_type": "authorization_code",
        "code": unquote(token),
        "client_id": environ.get("GOOGLE_CLIENT_ID"),
        "client_secret": environ.get("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": redirect_uri
    }
    launch = urlencode(sendoff).encode()
    request_send = Request("https://oauth2.googleapis.com/token", data=launch) # <urllib.request.Request object at 0x7f851dbaf670>
    response = urlopen(request_send) # error here
    response2 = response.read().decode("utf-8")
    parsed_response = loads(response2)
    access_token = parsed_response["access_token"]
    id_token = parsed_response["id_token"]


    request_with_id_token = Request(f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}")
    response3 = urlopen(request_with_id_token).read().decode("utf-8")
    parsed_response2 = loads(response3)
    print("-----id token get", parsed_response2)
    email = parsed_response2["email"]
    first_name = parsed_response2["given_name"]
    last_name = parsed_response2["family_name"]
    profile_photo = parsed_response2["picture"]

    return {"firstName": first_name, "lastName": last_name, "profilePhoto": profile_photo, "email": email}

@auth_routes.route("/googleSignIn/", methods=["POST"])
def google_sign_in():

    data = request.json
    token = data["code"]
    redirect_uri = data["redirect_URI"]
    sendoff = {
        "grant_type": "authorization_code",
        "code": unquote(token),
        "client_id": environ.get("GOOGLE_CLIENT_ID"),
        "client_secret": environ.get("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": redirect_uri
    }
    launch = urlencode(sendoff).encode()
    request_send = Request("https://oauth2.googleapis.com/token", data=launch)
    response = urlopen(request_send) # error used to be here
    response2 = response.read().decode("utf-8")
    parsed_response = loads(response2)
    id_token = parsed_response["id_token"]


    request_with_id_token = Request(f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}")
    response3 = urlopen(request_with_id_token).read().decode("utf-8")
    parsed_response2 = loads(response3)
    email = parsed_response2["email"]

    user = User.query.filter(User.email == email).first()
    if user:
        login_user(user)
        return user.to_dict()
    else:
        return {"errors": ["Cannot find a registered user from the provided LinkedIn credentials"]}, 400



	X1 + X2 + X5 + X6 + X7 >= 17 ;
      subject to Tuesday:
	X1 + X2 + X3 + X6 + X7 >= 13;
      subject to Wednesday:
	X1 + X2 + X3 + X4 + X7 >= 15;
      subject to Thursday:
	X1 + X2 + X3 + X4 + X5 >= 19;
      subject to Friday:
	X2 + X3 + X4 + X5 + X6 >= 14;
      subject to Saturday:
	X3 + X4 + X5 + X6+ X7 >= 16;
      subject to Sunday:
	X1 + X4 + X5 + X6 + X7 >= 11;