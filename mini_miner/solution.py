#!/usr/bin/env python3
import hashlib
import json

from _libs.python.request_handler import RequestHandler

PROBLEM_NAME = 'mini_miner'


def matches_difficulty(sha, difficulty):
    """Checks if the `sha` has the `difficulty` number of leading 0's."""

    num_bits = int(sha.hexdigest(), 16).bit_length()
    leading_zeros = 256 - num_bits

    return leading_zeros == difficulty


def solve(response):
    """
    Given the block and the difficulty, the nonce value must be made such that
    the final SHA256 must have `difficulty` number of _bits_ (not bytes or digits) at the beginning.
    """
    difficulty = response['difficulty']

    block = response['block']

    print(f"difficulty: {difficulty}")
    print(f"block: {block}")

    new_block = block.copy()  # Doesn't need to be a deep copy since we only change nonce value
    nonce = 0
    while nonce > -1:  # Always True, infinite loop until broken
        new_block['nonce'] = nonce
        jsonified = json.dumps(new_block, sort_keys=True, indent=None)

        sha = hashlib.sha256(jsonified.encode('ascii'))
        if matches_difficulty(sha, difficulty):
            print(f"jsonified: {jsonified}")
            print(f"sha: {sha.hexdigest()}")
            return nonce

        nonce += 1


if __name__ == '__main__':
    """https://hackattic.com/challenges/mini_miner"""

    # Setup
    request_handler = RequestHandler(problem_name=PROBLEM_NAME)
    response = request_handler.fetch_problem_set()
    # Solution
    nonce = solve(response=response.json())
    # Submit
    r = request_handler.submit_solution({'nonce': nonce})
    print(r.json())
