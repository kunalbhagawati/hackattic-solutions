import base64
import hashlib
import hmac
import scrypt as sc

from _libs.python.request_handler import RequestHandler

PROBLEM_NAME = 'password_hashing'


def solve(data):
    password = bytes(data['password'], 'utf-8')
    salt = base64.b64decode(bytes(data['salt'], 'utf-8'))
    pbkdf2 = data['pbkdf2']
    scrypt = data['scrypt']

    # check scrypt control matches against password="rosebud", salt="pepper", N=128, p=8, n=4
    control_hex = scrypt['_control']
    control_calculated = hashlib.scrypt(bytes("rosebud", 'utf-8'), salt=bytes("pepper", 'utf-8'), n=128, p=8, r=4, dklen=32)

    if control_calculated.hex() != control_hex:
        raise "Control check failed"

    sha256_ = hashlib.sha256(password)
    hmac_ = hmac.new(salt, password, hashlib.sha256)
    pbkdf2_ = hashlib.pbkdf2_hmac(pbkdf2['hash'], password, salt, pbkdf2['rounds'])
    scrypt_ = sc.hash(password, salt, N=scrypt['N'], p=scrypt['p'], r=scrypt['r'], buflen=scrypt['buflen'])

    return {
        'sha256': sha256_.hexdigest(),
        'hmac': hmac_.hexdigest(),
        'pbkdf2': pbkdf2_.hex(),
        'scrypt': scrypt_.hex(),
    }


if __name__ == '__main__':
    # Setup
    handler = RequestHandler(PROBLEM_NAME)
    response = handler.fetch_problem_set()
    # Solution
    hashes = solve(response.json())
    # Submit
    response = handler.submit_solution(hashes)
    print(response.json())
