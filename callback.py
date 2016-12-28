"""
Callback library for validations on information inbound
"""
import requests
import json
import base64
import time
import hmac
import jwt
from dotenv import Dotenv
import hashlib
from Crypto.Hash import SHA256 as sha256_module

class OIDCCallbackHandler(object):
    def __init__(self, client_id, client_secret, auth_0_domain):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_0_domain = auth_0_domain
        self.redirect_uri = self.__get_redirect_uri()

    def is_secure(self, token_info):
        """Convinience function to simplify controller\
        will check token expiration, validity against auth0\
        and finally token signing"""
        if self.__expiration(token_info) == True:
            return False
        elif self.__is_valid(token_info) == False:
            return False
        elif self.__is_signed_approriately(token_info) == False:
            return False
        else:
            return True

    def __is_missing_padding(self, data):
        """Returns how much padding missing depending on whether the length \
        can be modulus 4.  Solve B64 decode problem for string friendlieness"""
        missing_padding = len(data) % 4
        return missing_padding

    def __add_padding(self, data, missing_padding):
        data += b'='* (4 - missing_padding)
        return data

    def __is_signed_approriately(self, token_info):
        """Takes token info and returns whether the token is\
        correctly signed against auth0"""

        signature = str(token_info['id_token'].split('.')[2])
        payload = str(token_info['id_token'].split('.')[1])
        header = str(token_info['id_token'].split('.')[0])
        secret = self.client_secret
        secret = base64.urlsafe_b64decode(secret)


        this_signature = base64.urlsafe_b64encode(self.__generate_signature_for_token(
            (header + "." + payload),
            secret)
        )[:-1]

        if this_signature == signature:
            return True
        else:
            return False

    def __generate_signature_for_token(self, text, secret):
        """Auth0 is known to use hmac SHA256 for sigining\
        attempt to generate a matching hash"""
        signature =  hmac.new(
            secret,
            text,
            sha256_module
        ).digest()
        return signature

    def __expiration(self, token_info):
        """Takes token info and parses it to return the token expiration"""
        data = str(token_info['id_token'].split('.')[1])
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += b'='* (4 - missing_padding)
            data = json.loads(base64.decodestring(data))
        expiry = data['exp']

        """If expiry occurs before the current epoch time throw True\
        to indicate that the access token is expired an user should re-auth\
        """
        if expiry < time.time():
            return True
        else:
            return False
        pass

    def __is_valid(self, token_info):
        """Take a token and queries auth0 to see if the token is still valid"""
        try:
            if self.get_session_information(token_info)['email']:
                return True
            else:
                return False
        except:
            return False

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
            return userinfo
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
            raise error
            return None
            pass

    def __get_redirect_uri(self):
        """Returns a redirect URI from environment file """
        env = Dotenv('./.env')
        uri = env["AUTH0_CALLBACK_URL"]
        if uri is not None:
            return uri
        else:
            return "http://127.0.0.1:5000/callback"
