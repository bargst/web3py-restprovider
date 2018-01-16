from web3 import Web3, HTTPProvider
from flask import Flask, jsonify, request, abort
from datetime import datetime, timedelta
import json

RESTServer = Flask(__name__)
web3 = Web3()
blocks = {'last': None}


@RESTServer.route('/<method>')
def call(method):
    params = []

    arg_params = request.args.get('params')
    if arg_params:
        params = json.loads(arg_params)
    req_json = request.get_json()

    req_json = request.get_json()
    print(req_json)
    if req_json and 'params' in req_json:
        params = req_json['params']

    p = web3.providers[0]
    response = p.make_request(method, params)
    return jsonify(response)


@RESTServer.route('/provider')
def get_provider():
    p = web3.providers[0]
    if type(p) is HTTPProvider:
        return jsonify(f'HTTPProvider({p.endpoint_uri})')
    return jsonify('AutoProvider')


@RESTServer.route('/provider', methods=['PUT'])
def set_provider():
    req_json = request.get_json()
    if req_json and 'endpoint_uri' in req_json:
        web3.providers = [HTTPProvider(req_json['endpoint_uri'])]
    return get_provider()


@RESTServer.route('/healthcheck')
def healthcheck():
    syncing = web3.eth.syncing
    if syncing:
        abort(503)
    else:
        blocknumber = web3.eth.blockNumber
        now = datetime.now()

        if blocks['last'] is None:
            blocks['last'] = blocknumber

        # Detect a stalling node
        if blocknumber in blocks and now - blocks[blocknumber] > timedelta(seconds=30):
            #TODO manage reorg ....
            abort(503)

        blocks['last'] = blocknumber
        blocks[blocknumber] = now

        return jsonify({'syncing': syncing, 'blocknumber': blocknumber})
