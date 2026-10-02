import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)
TARGET = "https://api.pitchapi.dev"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    url = f"{TARGET}/{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        params=request.args,
        data=request.get_data(),
        timeout=30
    )
    excluded = {'content-encoding', 'transfer-encoding', 'connection'}
    headers = [(k, v) for k, v in resp.headers.items()
               if k.lower() not in excluded]
    return Response(resp.content, resp.status_code, headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
