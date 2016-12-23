"""
Flask app for Mozilla's IAM OpenID Connect Challenge
"""
import time

import os
import requests
from dotenv import Dotenv
from flask import Flask, render_template, request, jsonify, session, redirect, render_template, send_from_directory
from flask.ext.cors import cross_origin

#So I can add custom decorators
from functools import wraps

#My OIDCCallbackHandler
import callback

#Set the session type to be memory normally I would use redis
SESSION_TYPE = 'memcache'

env = None

try:
    env = Dotenv('./.env')
    client_id = env["AUTH0_CLIENT_ID"]
    client_secret = env["AUTH0_CLIENT_SECRET"]
    auth_0_domain = env["AUTH0_DOMAIN"]
    secret_key = env["SECRET_KEY"]
except IOError:
    env = os.environ

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates',
)

app.secret_key = secret_key


# Requires authentication decorator
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

@app.route('/callback')
def callback_handling():
  try:
      """Controller style wrapper to handle all callbacks"""
      code = request.args.get('code')
      handler = callback.OIDCCallbackHandler(
        client_id,
        client_secret,
        auth_0_domain
      )

      """Ask our custom handler to get the token payload"""
      token_payload = handler.generate_token_payload(code)

      """Ask our custom handler to send a post via requests \
      and return token info this contains our access token\
      we can then use the access_token to do additional things
      via the API like enumerate more information about the user"""
      token_info = handler.token_info(token_payload)

      """Pass our complete token info to the handler for follow up\
      info to store in session"""
      user_info = handler.get_session_information(token_info)

      """Store our user attributes in session"""
      session['profile'] = user_info

      return redirect('/supersecret')
  except:
      """If anything returns an error during this redirect to custom error"""
      return redirect('/error')

@app.route('/error', methods=['GET'])
def bad_things_happened():
    return render_template('error.html')

@app.route('/supersecret', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def secret():
    return render_template('secret.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'profile' in session:
        return redirect('/supersecret')
    else:
        session['profile'] = None
    return render_template('index.html', env=env, session=session['profile'])

if __name__ == '__main__':
    app.run(debug=True)
