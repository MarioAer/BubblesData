import os
from datetime import datetime
from flask import Flask, render_template, redirect, flash, abort, url_for, request
from flask.ext.restless import APIManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.login import UserMixin

from wtforms import form, fields, validators
from flask.ext import login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import helpers, expose, AdminIndexView
from werkzeug.security import generate_password_hash, check_password_hash

# Create Flask application
app = Flask(__name__)

# Create secrey key so we can use sessions
app.config['SECRET_KEY'] = os.urandom(24).encode('hex')

# Create in-memory database

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bubbles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# Flask-SQLAlchemy: Define a models
class BubblesUser(db.Model, UserMixin):
    __tablename__ = 'bubbles_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Unicode(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    role = db.Column(db.Unicode(50), nullable=False)
    experience_points = db.Column(db.Integer)
    skills = db.Column(db.Text)
    created_at = db.Column(db.Date)
    bubbles = db.relationship('BubblesBubble', backref='bubbles_users', lazy='dynamic')
    settings = db.relationship('BubblesUserSetting', backref='bubbles_users', uselist=False, lazy='select')
    resources = db.relationship('BubblesResource', backref='bubbles_users', lazy='dynamic')
    projects = db.relationship('BubblesProject', backref='bubbles_users', lazy='dynamic')
    quests = db.relationship('BubblesQuest', backref='bubbles_users', lazy='dynamic')

    def __repr__(self):
        return '<User: ' + str(self.name) + ' - Id: ' + str(self.id) + '>'

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class BubblesBubble(db.Model, UserMixin):
    __tablename__ = 'bubbles_bubbles'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('bubbles_projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('bubbles_users.id'))
    type = db.Column(db.String, default="bubble")
    order = db.Column(db.Integer, default=1)
    setting = db.relationship('BubblesSetting', backref='bubbles_bubbles', uselist=False, lazy='select')
    resources = db.relationship('BubblesResource', backref='bubbles_bubbles', uselist=False, lazy='select')

    def __repr__(self):
        return '<BubbleId: ' + str(self.id) + '>'


class BubblesMetaGlobal(db.Model, UserMixin):
    __tablename__ = 'bubbles_meta_global'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<BubblesMetaGlobal %r>' % str(self.name)


class BubblesPage(db.Model):
    __tablename__ = 'bubbles_pages'
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    meta_locals = db.relationship('BubblesMetaLocal', backref='bubbles_pages', lazy='dynamic')

    def __repr__(self):
        return '<BubblesPage %r>' % self.id


class BubblesMetaLocal(db.Model):
    __tablename__ = 'bubbles_meta_local'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    page = db.Column(db.Integer, db.ForeignKey('bubbles_pages.id'))
    content = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<BubblesMetaLocal %r>' % str(self.name)


bubbles_project_resource = db.Table('bubbles_project_resource',
                                    db.Column('project_id', db.Integer, db.ForeignKey('bubbles_projects.id')),
                                    db.Column('resource_id', db.Integer, db.ForeignKey('bubbles_resources.id'))
                                    )


class BubblesProject(db.Model):
    __tablename__ = 'bubbles_projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('bubbles_users.id'))
    bubbles = db.relationship('BubblesBubble', backref='bubbles_projects', lazy='dynamic')
    resources = db.relationship('BubblesResource', secondary=bubbles_project_resource,
                                backref=db.backref('bubbles_projects', lazy='dynamic'))

    def __repr__(self):
        return '<BubblesProject %r>' % str(self.id)


class BubblesQuest(db.Model):
    __tablename__ = 'bubbles_quests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('bubbles_users.id'))
    editor_id = db.Column(db.String(255), default="null")
    state = db.Column(db.String(45), nullable=False)
    resource = db.Column(db.String(255), default="null")
    language = db.Column(db.String(45), default="null")

    def __repr__(self):
        return '<BubblesQuestId %r>' % str(self.id)


class BubblesResource(db.Model):
    __tablename__ = 'bubbles_resources'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(45), nullable=False)
    data = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('bubbles_users.id'))
    bubble = db.Column(db.Integer, db.ForeignKey('bubbles_bubbles.id'))

    def __repr__(self):
        return '<BubblesResourceId %r>' % str(self.id)


class BubblesSettingCms(db.Model):
    __tablename__ = 'bubbles_settings_cms'
    id = db.Column(db.Integer, primary_key=True)
    property = db.Column(db.String(255))
    value = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Integer, nullable=False, default=1)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<BubblesSettingCms %r>' % self.property


class BubblesSetting(db.Model):
    __tablename__ = 'bubbles_settings'
    id = db.Column(db.Integer, primary_key=True)
    bubble_id = db.Column(db.Integer, db.ForeignKey('bubbles_bubbles.id'))
    size_x = db.Column(db.Integer, nullable=False)
    size_y = db.Column(db.Integer, nullable=False)
    bubbles_image = db.Column(db.String(255))

    def __repr__(self):
        return '<BubblesSetting %r>' % self.id


class BubblesUserSetting(db.Model):
    __tablename__ = 'bubbles_user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('bubbles_users.id'))
    avatar_image = db.Column(db.String(128))

    def __repr__(self):
        return '<BubblesUserSetting %r>' % self.id


class BubbleSkin(db.Model):
    __tablename__ = 'bubble_skins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    activated = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<BubbleSkin %r>' % self.id


class BubbleMessage(db.Model):
    __tablename__ = 'bubbles_messages'
    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('bubbles_users.id'), primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('bubbles_users.id'), primary_key=True)

    sender = db.relationship('BubblesUser', backref='sender_id', foreign_keys='BubbleMessage.sender_id')
    receiver = db.relationship('BubblesUser', backref='receiver_id', foreign_keys='BubbleMessage.receiver_id')

    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    viewed_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<BubbleMessage %r>' % self.id


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(BubblesUser).filter_by(password=self.password.data).first()


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(BubblesUser).get(user_id)


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
manager.create_api(BubbleMessage, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesUserSetting, methods=['GET', 'POST', 'DELETE', 'UPDATE'])
manager.create_api(BubblesSettingCms, methods=['GET', 'POST', 'DELETE', 'UPDATE'])

# Initialize flask-login
init_login()


# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated and (
        login.current_user.role == 'admin' or login.current_user.role == 'Admin')


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


admin = Admin(app, name='bubbles', template_mode='bootstrap3', index_view=MyAdminIndexView())

admin.add_view(MyModelView(BubblesUser, db.session))
admin.add_view(MyModelView(BubblesBubble, db.session))
admin.add_view(MyModelView(BubblesProject, db.session))
admin.add_view(MyModelView(BubblesQuest, db.session))
admin.add_view(MyModelView(BubblesResource, db.session))
admin.add_view(MyModelView(BubblesSetting, db.session))
admin.add_view(MyModelView(BubbleMessage, db.session))
admin.add_view(MyModelView(BubblesUserSetting, db.session))

admin.add_view(MyModelView(BubblesPage, db.session))
admin.add_view(MyModelView(BubblesMetaLocal, db.session))
admin.add_view(MyModelView(BubblesSettingCms, db.session))
admin.add_view(MyModelView(BubbleSkin, db.session))
admin.add_view(MyModelView(BubblesMetaGlobal, db.session))


@app.route("/")
def index():
    return render_template('index.html')


db.drop_all()
db.create_all()


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
