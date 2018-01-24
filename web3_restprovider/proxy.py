from .client import RESTProvider

import gevent
import gevent.queue

from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport
from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher

class RESTDispatcher(RPCDispatcher):

    def __init__(self, rest_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = RESTProvider(rest_url)

    def get_method(self, name):
        """
        Use provider to request the result of rpc method `name'
        """

        # Simple alias for provider method
        def provider_method(*args):
            request = self.provider.make_request(name, params=args)
            if 'result' in request:
                return request['result']
            elif 'error' in request:
                raise Exception(request['error'])

            return None

        return provider_method


class JSONRPCProxy:

    def __init__(self, rest_url=None):

        self.dispatcher = RESTDispatcher(rest_url)

        # TinyRPC WSGI App
        self.transport = WsgiServerTransport(queue_class=gevent.queue.Queue)
        self.wsgi_app = self.transport.handle

        # TinyRPC RPC Server
        self.rpc_server = RPCServerGreenlets(
            self.transport,
            JSONRPCProtocol(),
            self.dispatcher
        )
        gevent.spawn(self.rpc_server.serve_forever)

RESTProxy = JSONRPCProxy().wsgi_app
