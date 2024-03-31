#!/usr/bin/env python3
import base64
from struct import unpack

import requests

from _libs.python.url_builder import fetch_problem_inputs_url
from _libs.python.request_handler import RequestHandler

PROBLEM_NAME = "help_me_unpack"


def solve(problem):
    byte_string = base64.b64decode(problem['bytes'])
    pack_format = 'iIhfdd'
    unpacked = unpack(pack_format, byte_string)
    return {
        "int": unpacked[0],
        "uint": unpacked[1],
        "short": unpacked[2],
        "float": unpacked[3],
        "double": unpacked[4],
        "big_endian_double": unpack("!d", byte_string[-8:])[0]
    }


def get_base64_string():
    challenge_response = requests.get(fetch_problem_inputs_url(PROBLEM_NAME))
    if challenge_response.status_code // 100 != 2:
        raise RuntimeError(challenge_response.json())

    return challenge_response.json()['bytes']


if __name__ == '__main__':
    # Setup
    request_handler = RequestHandler(PROBLEM_NAME)
    response = request_handler.fetch_problem_set()
    # Solution
    sln_json = solve(response.json())
    r = request_handler.submit_solution(sln_json)
    print(r.json())
