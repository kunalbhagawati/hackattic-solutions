#!/usr/bin/env python3
import datetime
import pathlib
from io import BytesIO

import face_recognition
import requests
from PIL import Image

from common_python.request_handler import RequestHandler

ARTIFACTS_DIR_NAME = f"artifacts/{datetime.date.today().strftime('%d-%m-%y')}/"


def crop_from(image: Image.Image, row: int, col: int) -> Image.Image:
    w = image.width / 8
    h = image.height / 8

    left = col * w
    upper = row * h
    right = left + w
    lower = upper + h
    return image.crop([left, upper, right, lower])


def _save_image(image: Image.Image, name: str, format="png"):
    with open(f"{ARTIFACTS_DIR_NAME}/{name}.{format}", 'wb') as f:
        image.save(f)


def solve(image_url: str):
    img_raw = requests.get(image_url)
    buffer = BytesIO(img_raw.content)
    img = Image.open(buffer)

    with open(f"{ARTIFACTS_DIR_NAME}/image.png", 'wb') as f:
        img.save(f)

    res = []

    for row in range(0, 8):
        for col in range(0, 8):
            # get the sub-image from the main image
            i = crop_from(img, row, col)
            _save_image(i, f"{row}-{col}")
            fr_img = face_recognition.load_image_file(f"{ARTIFACTS_DIR_NAME}/{row}-{col}.png")
            locs = face_recognition.face_locations(fr_img)
            if len(locs) >= 1:
                res.append([row, col])

    return res


if __name__ == "__main__":
    """https://hackattic.com/challenges/basic_face_detection"""

    # Setup
    handler = RequestHandler("basic_face_detection")
    response = handler.fetch_problem_set()
    image_url = response.json()['image_url']
    print(image_url)

    pathlib.Path(ARTIFACTS_DIR_NAME).mkdir(parents=True, exist_ok=True)

    res = solve(image_url)
    print(res)
    response = handler.submit_solution({"face_tiles": res})
    print(response.json())
