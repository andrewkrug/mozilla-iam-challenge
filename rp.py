"""
Flask app for Mozilla's IAM OpenID Connect Challenge
"""
import time
import requests
import os
from dotenv import Dotenv
from flask import Flask, render_template, request, jsonify, session, redirect, render_template, send_from_directory

#So I can add custom decorators
from functools import wraps

env = None

try:
    env = Dotenv('./.env')
    client_id = env["AUTH0_CLIENT_ID"]
    client_secret = env["AUTH0_CLIENT_SECRET"]
    auth_0_domain = env["AUTH0_DOMAIN"]
except IOError:
    env = os.environ

app = Flask(__name__)


HOSTED_LOCK = 'https://{domain}/login?client={client_secret}'.format(
    domain=auth_0_domain,
    client_secret=client_id
)

# Requires authentication decorator
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      print(HOSTED_LOCK)
      # Redirect to Login page here
      return redirect(HOSTED_LOCK)
    return f(*args, **kwargs)

  return decorated

@app.route('/callback')
def callback_handling():
  code = request.args.get('code')
  json_header = {'content-type': 'application/json'}
  token_url = "https://{domain}/oauth/token".format(domain=AUTH_0_DOMAIN)

  token_payload = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri':  'https://127.0.0.1:5000/callback',
    'code':          code,
    'grant_type':    'authorization_code'
  }

  token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()

  user_url = "https://{domain}/userinfo?access_token={access_token}" \
      .format(domain=AUTH_0_DOMAIN, access_token=token_info['access_token'])

  user_info = requests.get(user_url).json()

  session['profile'] = user_info

  return redirect('/')

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
