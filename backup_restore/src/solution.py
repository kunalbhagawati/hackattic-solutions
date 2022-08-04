import base64
import gzip

import docker
import psycopg

from config import config
from request_handler import RequestHandler

PROBLEM_NAME = 'backup_restore'


def get_docker_container():
    docker_client = docker.from_env()
    return docker_client.containers.get(config.backup_restore__container_name)


def get_sql_string_from_data(data):
    # Data is base64 encoded.
    dump_bytes = base64.b64decode(data['dump'])
    # And also gzipped (Z9)
    return gzip.decompress(dump_bytes).decode('utf-8')


def restore_data(container, sql):
    """Runs the `psql` command on the container with the given dump as an sql string."""

    psql_cmd = f"""psql -U {config.postgres__username} -v -d {config.postgres__dbname} << EOF
{sql}
    EOF
    """

    # Assuming this will _always_ pass.
    return container.exec_run(['sh', "-c", psql_cmd])


def get_ssns(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT ssn FROM criminal_records where status='alive'
            """)

    return [i[0] for i in cur]


def solve(data):
    container = get_docker_container()
    sql = get_sql_string_from_data(data)
    restore_data(container, sql)

    conn_url = f"postgresql://{config.postgres__username}:{config.postgres__password}@{'127.0.0.1'}:{config.postgres__port}/{config.postgres__dbname}"
    with psycopg.connect(conn_url) as conn:
        return get_ssns(conn)


if __name__ == '__main__':
    # Setup
    handler = RequestHandler(PROBLEM_NAME)
    response = handler.fetch_problem_set()
    # Solution
    alive_ssns = solve(response.json())
    # Submit
    response = handler.submit_solution({"alive_ssns": alive_ssns})
    print(response.json())
