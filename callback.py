"""
Callback library for validations on information inbound
"""
import requests
import json
from dotenv import Dotenv



class OIDCCallbackHandler(object):
    def __init__(self, client_id, client_secret, auth_0_domain):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_0_domain = auth_0_domain
        self.redirect_uri = self.__get_redirect_uri()

    def get_session_information(self, token_info):
        """Takes token info and calls two subsequent methods to construct\
        the URL and validate the response"""
        url = self.__get_user_url(token_info['access_token'])
        userinfo = self.__get_user_info(url)
        return userinfo


    def __get_user_info(self, user_url):
        """Takes an access token and requests additional information about\
        the user form auth0"""
        try:
            userinfo = requests.get(user_url).json()
        except:
            #Add entry in stream logger that request did not complete
            return None
            pass

    def __get_user_url(self, access_token):
        """Takes an access token and returns the requesite URL"""
        user_url = "https://{domain}/userinfo?access_token={access_token}" \
              .format(
                domain=self.auth_0_domain, access_token=access_token
            )
        return user_url

    def generate_token_payload(self, code):
        """Generates a token payload from object"""
        token_payload = {
          'client_id': self.client_id,
          'client_secret': self.client_secret,
          'redirect_uri':  self.redirect_uri,
          'code':          code,
          'grant_type':    'authorization_code'
        }
        return token_payload

    def token_info(self, token_payload):
        """Takes a token payload and returns token_info"""
        try:
            token_url = "https://{domain}/oauth/token".format(
                domain=self.auth_0_domain
            )

            json_header = {'content-type': 'application/json'}
            token_info = requests.post(
                token_url,
                data=json.dumps(token_payload),
                headers = json_header
            ).json()
            return token_info
        except Exception as error:
            #Add entry in stream logger that token info was not parseable
            return None
            pass

    def __get_redirect_uri(self):
        """Returns a redirect URI from environment file """
        env = Dotenv('./.env')
        uri = env["AUTH0_CALLBACK_URL"]
        return uri
