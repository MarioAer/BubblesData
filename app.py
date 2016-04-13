import os
from flask import Flask, render_template, redirect, flash, abort, url_for
from flask.ext.restless import APIManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy

# Create Flask application
app = Flask(__name__)

# Create secrey key so we can use sessions
app.config['SECRET_KEY'] = os.urandom(24).encode('hex')

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bubbles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# Flask-SQLAlchemy: Define a models
class BubblesUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Unicode(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.Unicode(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    role = db.Column(db.Unicode(50), nullable=False)
    experience_points = db.Column(db.Integer)
    skills = db.Column(db.Text)
    bubbles = db.relationship('BubblesBubble', backref='bubbles_user', lazy='dynamic')
    messages = db.relationship('BubbleMessage', backref='bubbles_user', lazy='dynamic')
    settings = db.relationship('BubblesUserSetting', backref='bubbles_user', uselist=False, lazy='select')
    resources = db.relationship('BubblesResource', backref='bubbles_user', lazy='dynamic')
    projects = db.relationship('BubblesProject', backref='bubbles_user', lazy='dynamic')

    def __str__(self):
        return str(self.id) + " " + self.name


class BubblesBubble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('bubbles_project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('bubbles_user.id'))
    type = db.Column(db.VARCHAR, default="bubble")
    order = db.Column(db.Integer, default=1)

    def __str__(self):
        return self.id


class BubblesMetaGlobal(db.Model):
    name = db.Column(db.VARCHAR(30), primary_key=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __str__(self):
        return self.name


class BubblesMetaLocal(db.Model):
    name = db.Column(db.VARCHAR, primary_key=True, nullable=False)
    page = db.Column(db.Integer, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)


class BubblesPage(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    alias = db.Column(db.VARCHAR, nullable=False)
    title = db.Column(db.VARCHAR, nullable=False)


class BubblesProject(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('bubbles_user.id'))
    bubbles = db.relationship('BubblesBubble', backref='bubbles_project', uselist=False, lazy='select')

    def __str__(self):
        return self.name


# class BubblesProjectsResource(db.Model):
#     __tablename__ = "bubbles_project_resources"
#     project_id = db.Column(db.Integer, nullable=False)
#     resource_id = db.Column(db.Integer, nullable=False)
#

class BubblesQuest(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR(45))
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer)
    editor_id = db.Column(db.VARCHAR(255), default="Null")
    state = db.Column(db.VARCHAR(45), nullable=False)
    resource = db.Column(db.VARCHAR(255), default="Null")
    language = db.Column(db.VARCHAR(45), default="Null")

    def __str__(self):
        return self.id


class BubblesResource(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.VARCHAR(45), nullable=False)
    data = db.Column(db.VARCHAR(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('bubbles_user.id'))


class BubblesSetting(db.Model):
    property = db.Column(db.VARCHAR(255), primary_key=True, nullable=False)
    value = db.Column(db.VARCHAR(255), nullable=False)
    activated = db.Column(db.Integer, nullable=False, default=1)
    description = db.Column(db.VARCHAR(255), nullable=False)


class BubblesUserSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('bubbles_user.id'))
    avatar_image = db.Column(db.String(128))


class BubbleSkin(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR(30), nullable=False)


class BubbleMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('bubbles_user.id'))
    receiver_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    viewed_at = db.Column(db.DateTime)


db.create_all()

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(BubblesUser, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesBubble, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesMetaGlobal, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesMetaLocal, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesPage, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesProject, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesQuest, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesResource, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesSetting, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubbleSkin, methods=['GET', 'POST', 'DELETE', 'UPDATE'])

admin = Admin(app, name='bubbles', template_mode='bootstrap3')
admin.add_view(ModelView(BubblesUser, db.session))
admin.add_view(ModelView(BubblesBubble, db.session))
admin.add_view(ModelView(BubblesMetaGlobal, db.session))
admin.add_view(ModelView(BubblesMetaLocal, db.session))
admin.add_view(ModelView(BubblesPage, db.session))
admin.add_view(ModelView(BubblesProject, db.session))
admin.add_view(ModelView(BubblesQuest, db.session))
admin.add_view(ModelView(BubblesResource, db.session))
admin.add_view(ModelView(BubblesSetting, db.session))
admin.add_view(ModelView(BubbleSkin, db.session))


@app.route("/")
def hello():
    return "Hello API"


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
