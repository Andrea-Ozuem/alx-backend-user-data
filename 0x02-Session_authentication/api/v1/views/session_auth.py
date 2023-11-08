#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def sess_login() -> str:
    '''handles login'''
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    u = User.search({'email': email})
    if not u:
        return jsonify({"error": "no user found for this email"}), 400
    u = u[0]
    if not u.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    sess_id = auth.create_session(u.id)
    res = jsonify(u.to_json())
    res.set_cookie('SESSION_NAME', sess_id)
    return res
