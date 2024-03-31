import os
from string import Template

from dotenv import load_dotenv

load_dotenv()

HOST = "https://hackattic.com"
CHALLENGE_PATH = "challenges/$PROBLEM_NAME"  # This is a pure string.
FETCH_PROBLEM_INPUTS_URL = Template(f"{HOST}/{CHALLENGE_PATH}/problem?access_token=$ACCESS_TOKEN")
SUBMIT_SOLUTION_URL = Template(f"{HOST}/{CHALLENGE_PATH}/solve?access_token=$ACCESS_TOKEN")


def fetch_problem_inputs_url(problem_name: str):
    return FETCH_PROBLEM_INPUTS_URL.substitute(PROBLEM_NAME=problem_name, ACCESS_TOKEN=os.environ['ACCESS_TOKEN'])


def submit_solution_url(problem_name: str):
    return SUBMIT_SOLUTION_URL.substitute(PROBLEM_NAME=problem_name, ACCESS_TOKEN=os.environ['ACCESS_TOKEN'])
