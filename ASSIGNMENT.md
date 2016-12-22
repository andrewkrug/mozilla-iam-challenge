Mozilla IAM Coding challenge
============================

This challenge is designed to be completed in 1 to 4h depending on your current knowledge of Python and OpenID Connect.
The result of the challenge must be licensed under the MPL (https://www.mozilla.org/en-US/MPL/).
The code must be written in Python (2 or 3 at your convenience).
The code may not use libraries such as pyoidc to call the OpenID Connect endpoints (run the HTTP calls yourself instead).

We understand that you will do your best to have a functional and readable example, with organized commits for us to look at.

Challenge
----------

Write code for authenticating a GitHub user to relying party (a web-server with a dummy page) using Auth0 as an OpenID Connect provider.

The resulting setup must:

- Use an Auth0 free account (https://auth0.com/ click "using auth0 for free" to sign-up, then create a client that uses GitHub social login)
- Start the relying party (RP) as a python web-server locally
- Use the "Authorization code flow" (This is an OpenID Connect term for how the authentication flow works)
- Show the stock Auth0 login screen called Lock (https://auth0.com/docs/libraries/lock) (this can be a redirect to the Auth0 hosted lock)
- Authenticate a GitHub user (You can create a free GitHub user on https://github.com if needed)
- Return to the RP local web-server and show a page displaying something such as "Hello world!"

Optional:
- Validate the identity passed by the OpenID Connect provider (auth0)
- Ensure CSRF protection is used
- Follow web security guidelines
- Show the user profile and/or id_token contents on the page when logged in

Your solution
-------------
Your solution is the python code for the RP, and any Javascript/NodeJS that you may have used within Auth0.
Please provide us with a link to that code so that we can review it.

Thanks and good luck!


Documentation
-------------
These links should help you get started:
- https://auth0.com/
- https://wiki.mozilla.org/Security/Guidelines/OpenID_Connect
- http://wiki.mozilla.org/Security/Guidelines/Web_Security
- https://en.wikipedia.org/wiki/OpenID_Connect
