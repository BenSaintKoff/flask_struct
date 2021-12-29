from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mpe.0123456789@localhost:5432/angalia'
app.config['SECRET_KEY'] = 'lgoprogram'
db = SQLAlchemy(app)
admin = Admin(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    nom = db.Column(db.String(20))
    prenom = db.Column(db.String(50))
    mail = db.Column(db.String(100))
    matricule = db.Column(db.String(10))
    mot_de_passe = db.Column(db.String(255))
    role = db.relationship('Role', secondary='user_roles')
    #role_id = db.Column(db.Integer(), db.Foreignkey('roles.id', ondelete='CASCADE'))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<Role {}>".format(self.name)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(UserRoles, db.session))

if __name__ == '__main__':
    app.run(debug=True)




