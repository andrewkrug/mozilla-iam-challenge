"""
Flask app for Mozilla's IAM OpenID Connect Challenge
"""
import time
import requests
import os
import json
from dotenv import Dotenv
from flask import Flask, render_template, request, jsonify, session, redirect, render_template, send_from_directory

#So I can add custom decorators
from functools import wraps

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
  code = request.args.get('code')
  json_header = {'content-type': 'application/json'}
  token_url = "https://{domain}/oauth/token".format(domain=auth_0_domain)

  token_payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri':  'http://127.0.0.1:5000/callback',
    'code':          code,
    'grant_type':    'authorization_code'
  }

  token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()

  print(token_payload)
  print(token_info)

  user_url = "https://{domain}/userinfo?access_token={access_token}" \
      .format(domain=auth_0_domain, access_token=token_info['access_token'])

  user_info = requests.get(user_url).json()

  session['profile'] = user_info

  return redirect('/')

@app.route('/supersecret', methods=['GET'])
@requires_auth
def secret():
    return render_template('secret.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'profile' in session:
        return redirect('/supersecret')
    return render_template('index.html', env=env)

if __name__ == '__main__':
    app.run(debug=True)
