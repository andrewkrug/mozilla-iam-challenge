# Mozilla Foundation IAM Test
# Running this project ( in a production way )
This is not really flaskified in production... because of the lack of unicorn and such.

However you may elect to run this from the Docker container that's been prepared for you.

Note: __Regardless of how you run this you'll need to craft an environment file__

_A sample environment file has been provided for convinience_

```
 docker run  -v `pwd`:/app/ -p 5000:5000 andrewkrug/mozilla-iam-challenge:latest
 ```

#Based on the challenge instructions available here:
[Assignment]('https://gist.github.com/jeffbryner/2792488ed4c26b47656e592322cbe6cb') https://gist.github.com/jeffbryner/2792488ed4c26b47656e592322cbe6cb

## Caveats

1. Some hard coded urls point callbacks to http://127.0.0.1:5000
2. Assumes some app setup on your part via Auth0. (_Github client secrets copy and paste with whitespace at the beginning so beware.  Auth0 does not strip these._)
3. Signature validation is working  ... the hard manual way.  Not using JWT parsing.  ( Not a caveat just plain neat )

## How to run test suite

### Note: Testing is relatively minimal and only exists to demonstrate an understanding of integrating a ruby style test watcher for TDD.

1. Setup a python virtual env `virtualenv .`
2. `source bin/activate`
3. Run nose `nosetests --with-watch`
