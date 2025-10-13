from flask import Blueprint, request, Response
import requests

endorsement_bp = Blueprint('endorsement_proxy', __name__)

@endorsement_bp.route('/endorsement-service/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    service_url = f'http://127.0.0.1:8001/{path}'
    
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    
    resp = requests.request(
        method=request.method,
        url=service_url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response
