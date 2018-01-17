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

## High Availability Deployment of RESTServer with HAProxy

Assuming 2 local RESTServer listening on localhost port 8081 and 8082 (forwarding request to different ethereum node), basic haproxy.conf :
```
global
    maxconn     20000
    log         127.0.0.1 local0
    user        haproxy
    chroot      /usr/share/haproxy
    pidfile     /run/haproxy.pid
    daemon

frontend  main
    bind :8080
    mode                 http
    log                  global
    option               httplog
    option               dontlognull
    option               http_proxy
    option forwardfor    except 127.0.0.0/8
    maxconn              8000
    timeout              client  30s

    default_backend             app

backend app
    mode        http
    balance     roundrobin
    timeout     connect 5s
    timeout     server  30s
    timeout     queue   30s
    server  app1 127.0.0.1:8081 check
    server  app2 127.0.0.1:8082 check
    option httpchk get /healthcheck
    http-check expect status 200
    default-server inter 3s fall 3 rise 2
```

## High Availability Deployment of RESTServer with Traefik and Consul

TODO
