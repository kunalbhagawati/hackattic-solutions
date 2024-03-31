#!/usr/bin/env python3
import asyncio
import datetime
import pathlib
import time
from io import BytesIO

import cv2
import requests
from PIL import Image

from _libs.python.request_handler import RequestHandler

ARTIFACTS_DIR_NAME = f"_artifacts/{datetime.date.today().strftime('%d-%m-%y')}/"

CLASSIFIER = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def _crop_from(image: Image.Image, row: int, col: int) -> Image.Image:
    w = image.width / 8
    h = image.height / 8

    left = col * w
    upper = row * h
    right = left + w
    lower = upper + h
    return image.crop([left, upper, right, lower])


async def _save_image(image: Image.Image, name: str, format="png"):
    with open(f"{ARTIFACTS_DIR_NAME}/{name}.{format}", 'wb') as f:
        image.save(f)


async def _is_face(image: Image.Image, row: int, col: int) -> bool:
    # get the sub-image from the main image
    cropped = _crop_from(image, row, col)

    # Convert to lib compatible image. ---
    await _save_image(cropped, f"{row}-{col}")

    img_arr = cv2.imread(f"{ARTIFACTS_DIR_NAME}/{row}-{col}.png")
    greyed = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    # ---

    locs = CLASSIFIER.detectMultiScale(greyed, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    return len(locs) >= 1


async def solve(image_url: str):
    img_raw = requests.get(image_url)
    buffer = BytesIO(img_raw.content)
    img = Image.open(buffer)
    await _save_image(img, f"image")

    res = []

    for row in range(0, 8):
        for col in range(0, 8):
            if await _is_face(image=img, row=row, col=col):
                res.append([row, col])

    return res


async def main():
    print(int(time.time()))

    # Setup
    handler = RequestHandler("basic_face_detection")
    response = handler.fetch_problem_set()
    image_url = response.json()['image_url']
    print(image_url)

    pathlib.Path(ARTIFACTS_DIR_NAME).mkdir(parents=True, exist_ok=True)

    res = await solve(image_url)
    print(res)
    response = handler.submit_solution({"face_tiles": res})
    print(response.json())


if __name__ == "__main__":
    """https://hackattic.com/challenges/basic_face_detection"""

    asyncio.run(main())
