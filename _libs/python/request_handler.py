import requests

from .url_builder import fetch_problem_inputs_url, submit_solution_url


class RequestHandler:
    """Handles the requests to and from the h^ server."""

    problem_name: str

    def __init__(self, problem_name):
        self.problem_name = problem_name

    @property
    def _fetch_url(self):
        return fetch_problem_inputs_url(problem_name=self.problem_name)

    @property
    def _submit_url(self):
        return submit_solution_url(problem_name=self.problem_name)

    def fetch_problem_set(self):
        response = requests.get(self._fetch_url)
        if response.status_code // 100 != 2:
            raise RuntimeError(response.json())  # Change to more specific errors later if needed.

        return response

    def submit_solution(self, json):
        response = requests.post(self._submit_url, json=json)
        if response.status_code // 100 != 2:
            raise RuntimeError(response.json())  # Change to more specific errors later if needed.

        return response
