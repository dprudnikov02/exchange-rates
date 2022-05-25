from datetime import datetime
import requests


def get_response(url, payload):
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        raise Exception(f"Request Error {response.status_code}")

    return response.json()


def transform_response(data, payload):
    requested_base = payload.get('base')
    requested_target = payload.get('symbols')
    if requested_base != data['base']:
        raise Exception(f"Requested base wasn't found")
    elif requested_target not in data['rates']:
        raise Exception(f"Requested target wasn't found")

    return requested_base, requested_target, str(datetime.now()), data['rates'][requested_target]
