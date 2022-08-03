import cv2
import requests
from common_python.url_builder import fetch_problem_inputs_url, submit_solution_url

PROBLEM_NAME = "reading_qr"
PNG_FILE_NAME = 'png.png'


def get_qr_code_image():
    """Get the png image from problem server as a binary stream."""

    challenge_response = requests.get(fetch_problem_inputs_url(PROBLEM_NAME))
    if challenge_response.status_code // 100 != 2:
        raise RuntimeError(challenge_response.json())

    image_url = challenge_response.json()['image_url']
    img_response = requests.get(image_url)
    if img_response.status_code // 100 != 2:
        return RuntimeError(img_response.json())

    return img_response.content


def extract_qr_code_from_png(img: bytes):
    with open(PNG_FILE_NAME, "wb") as f:
        f.write(img)

    img = cv2.imread("test.png")
    detector = cv2.QRCodeDetector()
    return detector.detectAndDecode(img)


def post_solution(code):
    response = requests.post(submit_solution_url(PROBLEM_NAME), json={'code': code})
    if response.status_code // 100 != 2:
        return RuntimeError(response.json())
    return response.json()


def main():
    img = get_qr_code_image()
    code_to_retrieve, _, _ = extract_qr_code_from_png(img)
    response = post_solution(code_to_retrieve)
    print(response)


if __name__ == '__main__':
    main()
