import json
import os
from flask import request, _request_ctx_stack, render_template, abort, \
    session, redirect, flash
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ

# COFFEESHOP PROJECT BOILERPLATE + AUTH0 Boilerplate for requires_auth()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = 'squirrel'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
  Get the header from the request
  it should raise an AuthError if no header is present
  it should attempt to split bearer and the token
  it should raise an AuthError if the header is malformed
  return the token part of the header
'''


def get_token_auth_header():
    #     """Obtains the Access Token from Authorization Header
    #     """
    if "Authorization" in request.headers:
        auth_header = request.headers["Authorization"]
        if auth_header:
            bearer_token_array = auth_header.split(' ')
            if bearer_token_array[0] and bearer_token_array[0].lower(
            ) == "bearer" and bearer_token_array[1]:
                return bearer_token_array[1]
    print('JWT not found')
    raise AuthError({
        'success': False,
        'message': 'JWT not found',
        'error': 401
    }, 401)


'''
    @INPUTS
        permission: string permission  (i.e. 'post:drink')
        payload: decoded jwt payload
    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in
      the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        print('permissions not in payload')
        abort(400)

    if permission not in payload['permissions']:
        print(f'{permission} not in {payload["permissions"]}')
        raise AuthError({
            'success': False,
            'message': 'Permission not found in JWT',
            'error': 401
        }, 401)

    return True


'''
    @INPUTS
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
'''


def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    print(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'success': False,
            'message': 'Authorization malformed',
            'error': 401,
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

    # Verify
    if rsa_key:
        print('rsa_key exists')
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            print("token expired")

            raise AuthError({
                'success': False,
                'message': 'Token expired',
                'error': 401,
            }, 401)

        except jwt.JWTClaimsError:
            print("Incorrect claims. Please, check the audience and issuer")
            raise AuthError({
                'success': False,
                'message': 'Incorrect claims. Please, check audience & issuer',
                'error': 401,
            }, 401)

        except Exception:
            raise AuthError({
                'success': False,
                'message': 'Unable to parse authentication token',
                'error': 400,
            }, 400)

    raise AuthError({
        'success': False,
        'message': 'Unable to find the appropriate key',
        'error': 400,
    }, 400)


'''
@implement @requires_auth(permission) decorator method
    @INPUTS
    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method
      validate claims and check the requested permission
    return the decorator which passes decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session:
                try:
                    token = None
                    if session['token']:
                        token = session['token']
                    else:
                        token = get_token_auth_header()
                        print('token at authorization time: {}'.format(token))
                    if token is None:
                        flash('You must be logged in to do this.')
                        abort(400)
                    payload = verify_decode_jwt(token)
                    print('Payload is: {}'.format(payload))
                    print(f'testing for permission: {permission}')
                    if check_permissions(permission, payload):
                        print('Permission is in permissions!')
                    return f(payload, *args, **kwargs)
                except Exception as e:
                    flash('You do not have the correct \
                        permissions to do this.')
                    # return render_template('index.html',
                    # userinfo=session['profile'])
                    abort(401)
            else:
                flash('You must be logged in to do this.')
                return render_template('index.html', userinfo='')
        return wrapper
    return requires_auth_decorator


def requires_auth_auth0(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session:
                flash('You are not logged in?.')
                # Redirect to Login page here
                return render_template('index.html', userinfo='')
            return f(*args, **kwargs)
        return decorated
    return requires_auth_decorator
