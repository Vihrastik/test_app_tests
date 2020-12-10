import requests

import settings
from src.common.consts import TemplException


def make_request(method, path, **kwargs):
    url = settings.BASE_URL + path
    try:
        res = requests.request(method, url, **kwargs)
    except ConnectionError as e:
        raise TemplException(f'Неудачная попытка запроса к {url}') from e
    return res


def upload_template(file_name: str, file: str, data: dict=None):
    files = {'file': (file_name, file)}
    data = data
    r = make_request('PUT', path='api/v1/templates', files=files, data=data, verify=False)
    return r


def get_templates_list():
    r = make_request('GET', path='/api/v1/templates')
    return r


def delete_template(tmpl_id: str):
    r = make_request('DELETE', path=f'/api/v1/templates/{tmpl_id}')
    return r


def install_template(tmpl_id: str):
    r = make_request('POST', path=f'/api/v1/templates/{tmpl_id}/install')
    return r
