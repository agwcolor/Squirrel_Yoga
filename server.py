# /server.py

from functools import wraps
import json
import os
from os import environ as env
from werkzeug.exceptions import HTTPException
from flask import request, abort, _request_ctx_stack
from jose import jwt
from urllib.request import urlopen

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode


AUTH0_DOMAIN = os.environ.get('API_BASE_URL')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.environ.get('API_AUDIENCE')




class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

'''
get header from request
'''
'''
def get_token_auth_header():
    # unpack request header
    if 'Authorization' not in request.headers:
        abort(401)
    # headers dict containing all fo the headers, like content-type etc.
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')  # only returns token, not bearer
    if len(header_parts) != 2:
        abort(401)  # malformed header
    elif header_parts[0].lower() != 'bearer':
        abort(401)
    return header_parts[1]  # token itself
'''

def get_token_auth_header():
    auth_header = request.headers.get("Authorization", None)
    if auth_header is None:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization Header is required."
        }, 401)
    auth_header_values = auth_header.split(" ")
    if len(auth_header_values) != 2:
        raise AuthError({
            "code": "invalid_authorization_header",
            "description": "Authorization Header is malformed."
        }, 401)
    elif auth_header_values[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_authorization_header",
            "description": "Authorization Header must start with \"Bearer\"."
        }, 401)
    return auth_header_values[1]
'''
check if permission in payload
'''

def check_permissions(permission, payload):
    if 'permissions' not in payload:  # does payload contain permissions key?
        abort(400)
    if permission not in payload['permissions']:
        abort(403)
    return True


'''
input : json web token
return: decoded payload
'''

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the \
                    audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)

'''
auth0 version
'''
def requires_auth(permission=''):

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session:
                print(session, " is the session")
                # Redirect to Login page here
                return redirect('/')
            return f(*args, **kwargs)
        return decorated

    return requires_auth


'''
coffeeshop version
'''

'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            print(payload, "is the payload")
            return f(payload, *args, **kwargs)
             
        return wrapper
    return requires_auth_decorator
    
'''