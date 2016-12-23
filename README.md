# Mozilla Foundation IAM Test
# Running this project ( in a production way )

#Based on the challenge instructions available here:
[Assignment]('https://gist.github.com/jeffbryner/2792488ed4c26b47656e592322cbe6cb') https://gist.github.com/jeffbryner/2792488ed4c26b47656e592322cbe6cb

## Caveats

1. Some hard coded urls point callbacks to http://127.0.0.1:5000
2. Assumes some app setup on your part via Auth0. (_Github client secrets copy and paste with whitespace at the beginning so beware.  Auth0 does not strip these._)

## How to run test suite

1. Setup a python virtual env `virtualenv .`
2. `source bin/activate`
3. Run nose `nosetests --with-watch`
