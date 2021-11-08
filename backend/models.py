""" db model for nft marketplace """
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


""" user template from previous apps, params are adjustable """


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    account_status = db.Column(db.String, nullable=True)
    profile_photo = db.Column(
        db.String(255), nullable=False, default="https://i.imgur.com/tdi3NGa.jpg")
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "profilePhoto": self.profile_photo,
            "accountStatus": self.account_status if self.account_status else "",
        }
