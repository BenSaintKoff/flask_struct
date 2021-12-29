from sqlalchemy.ext.declarative import declarative_base
from flask import Blueprint, render_template, redirect, request, flash, jsonify, g
from flask_login import login_user, logout_user, login_required
from .tables.models import User, UserRoles, Role
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity,
                                set_access_cookies,
                                set_refresh_cookies,
                                unset_jwt_cookies)

from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login_admin')
def login():
    return render_template('login.html')


@auth.route('/process', methods=['GET', 'POST'])
def login_post():
    username = request.form.get('username')

    password = request.form.get('password')

    users = User.query.filter_by(matricule=username)
    passw = False
    user = None
    ''' for u in users:
        if check_password_hash(u.mot_de_passe, password):
            user = u
            break'''
    for u in users:
        if u.mot_de_passe == password:
            user = u
            break

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if(not user):
        flash("S'il vous plait vérifier vos accès et réessayer encore.")
        return redirect('/login_admin') # if user doesn't exist or password is wrong, reload the page

    else:
        login_user(user)
        return redirect('/admin')

    # if the above check passes, then we know the user has the right credentials

    return redirect('/login_admin')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login_admin')


@auth.route('/api/login', methods=['POST'])
def api_login():
    login_json = request.get_json()

    if not login_json:
        return jsonify({'msg': 'MissingJSON'}), 400

    username = login_json.get('username')
    password = login_json.get('password')

    if not username:
        return jsonify({'msg': 'Username is missing'}), 400

    if not password:
        return jsonify({'msg': 'Password is missing'}), 400

    # user_password = User.query.filter_by(username=username).first().password
    user = User.query.filter_by(matricule=username).first()

    if (not user) | ((user.mot_de_passe, password) == False):
        return jsonify({'msg': 'Bad username or password'}), 401

    user_role = UserRoles.query.filter_by(user_id=int(user.id))
    role = []
    for ur in user_role:
        r = Role.query.filter_by(id=ur.role_id).first()
        role.append(r.name)

    user_claims = {'nom': user.nom, 'prenom': user.prenom, 'code_acces': username, 'role': role}

    expires = datetime.timedelta(hours=2)

    access_token = create_access_token(identity=username, additional_claims=user_claims, expires_delta=expires)
    refresh_token = create_refresh_token(identity=username, additional_claims=user_claims, expires_delta=expires)

    g.track_var['user'] = username

    resp = jsonify({'login': True, 'access': 'ok', 'role': role, 'access_token': access_token, 'refresh_token': refresh_token})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200


@auth.route('/api/token/remove', methods=['POST'])
def api_logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


