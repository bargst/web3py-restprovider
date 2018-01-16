# Web3 Python Rest Provider

Project composed by a RESTProvider directly usable with Web3() from web3.py python module.
And a demo REST server implementation using Flask.

## Setup

Requirement : python3 and pipenv
```
make env
```

## Using RESTProvider

```
from web3 import Web3
from web3_restprovider import RESTProvider

web3 = Web3(RESTProvider('http://localhost:8080')
```

## Start a RESTServer with gevent

```
from gevent.wsgi import WSGIServer
from web3_restprovider import RESTServer

http_server = WSGIServer(('', 8080), RESTServer)
http_server.serve_forever()
```

## Start a RESTServer with uwsgi
```
uwsgi --http-socket localhost:8080 --plugin python --manage-script-name --mount /=web3_restprovider:RESTServer --virtualenv $(pipenv --venv)
```

## High Availability Deployment of RESTServer with Traefik and Consul

TODO
