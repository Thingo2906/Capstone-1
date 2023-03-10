
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement= True)

    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")

    user_bmi = db.relationship('UserBMI')
    
    posts = db.relationship('Post')

    #likes = db.relationship('Post', secondary="likes")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, password, email, first_name, last_name, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url

        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class UserBMI(db.Model):
    """table of user's BMI result"""
    __tablename__="bmi_results"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    age = db.Column(db.Integer, nullable = False)
    weight = db.Column(db.Integer, nullable = False)
    height = db.Column(db.Float, nullable = False)
    bmi = db.Column(db.Float, nullable = False)
    health_condition = db.Column(db.Text, nullable= False)
    result_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user = db.relationship('User')

class Post(db.Model):
    """Share user health story, favorite food, halthy tips"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement =True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
   
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,
    )

    user = db.relationship('User')

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

    if __name__ == '__main__':
        app.run()
