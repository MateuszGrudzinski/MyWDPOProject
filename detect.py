import glob
import json
from pathlib import Path
from typing import Dict
import click
import cv2
import numpy as np
from tqdm import tqdm


def detect(img_path: str) -> Dict[str, int]:
    """Object detection function, according to the project description, to implement.

    Parameters
    ----------
    img_path : str
        Path to processed image.

    Returns
    -------
    Dict[str, int]
        Dictionary with quantity of each object.
    """
    #TODO: Implement detection method.


    cv2.namedWindow('org', cv2.WINDOW_NORMAL)
    cv2.namedWindow('threshold_y', cv2.WINDOW_NORMAL)
    cv2.namedWindow('canny_y', cv2.WINDOW_NORMAL)
    cv2.namedWindow('threshold_g', cv2.WINDOW_NORMAL)
    cv2.namedWindow('threshold_p', cv2.WINDOW_NORMAL)
    cv2.namedWindow('threshold_r', cv2.WINDOW_NORMAL)

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    blur = cv2.GaussianBlur(img,(7,7),0)
    img_hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    minhsv_y = np.array([20, 100, 100])
    maxhsv_y = np.array([30, 255, 255])
    maskhsv = cv2.inRange(img_hsv, minhsv_y, maxhsv_y)
    resulthsv = cv2.bitwise_and(img_hsv, img_hsv, mask=maskhsv)
    yellow_img_raw = cv2.cvtColor(resulthsv, cv2.COLOR_HSV2BGR)
    yellow_img = cv2.medianBlur(yellow_img_raw,5)
    yellow_canny = cv2.Canny(yellow_img, 10, 150, 3)
    dilated_y = cv2.dilate(yellow_canny, (1, 1), iterations=0)

    (cnt, hierarchy) = cv2.findContours(
        dilated_y.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    print(len(cnt))

    minhsv_g = np.array([35, 30, 30])
    maxhsv_g = np.array([65, 255, 255])
    maskhsv = cv2.inRange(img_hsv, minhsv_g, maxhsv_g)
    resulthsv = cv2.bitwise_and(img_hsv, img_hsv, mask=maskhsv)
    green_img = cv2.cvtColor(resulthsv, cv2.COLOR_HSV2BGR)

    minhsv_p = np.array([150, 20, 20])
    maxhsv_p = np.array([170, 255, 255])
    maskhsv = cv2.inRange(img_hsv, minhsv_p, maxhsv_p)
    resulthsv = cv2.bitwise_and(img_hsv, img_hsv, mask=maskhsv)
    purple_img = cv2.cvtColor(resulthsv, cv2.COLOR_HSV2BGR)

    minhsv_r = np.array([176, 100, 100])
    maxhsv_r = np.array([179, 200, 200])
    maskhsv1 = cv2.inRange(img_hsv, minhsv_r, maxhsv_r)
    minhsv_r = np.array([0, 50, 50])
    maxhsv_r = np.array([10, 255, 255])
    maskhsv2 = cv2.inRange(img_hsv, minhsv_r, maxhsv_r)
    maskhsv = cv2.bitwise_or(maskhsv1, maskhsv2)
    resulthsv = cv2.bitwise_and(img_hsv, img_hsv, mask=maskhsv)
    red_img = cv2.cvtColor(resulthsv, cv2.COLOR_HSV2BGR)

    cv2.imshow('org', img)
    cv2.imshow('threshold_y', yellow_img)
    cv2.imshow('canny_y', yellow_canny)
    cv2.imshow('threshold_g', green_img)
    cv2.imshow('threshold_p', purple_img)
    cv2.imshow('threshold_r', red_img)

    cv2.waitKey(0)

    red = 0
    yellow = 0
    green = 0
    purple = 0

    return {'red': red, 'yellow': yellow, 'green': green, 'purple': purple}


@click.command()
@click.option('-p', '--data_path', help='Path to data directory', type=click.Path(exists=True, file_okay=False, path_type=Path), required=True)
@click.option('-o', '--output_file_path', help='Path to output file', type=click.Path(dir_okay=False, path_type=Path), required=True)
def main(data_path: Path, output_file_path: Path):

    temp_path1 = Path(data_path.decode('utf-8'))
    img_list = temp_path1.glob('*.jpg')
    results = {}

    for img_path in tqdm(sorted(img_list)):
        fruits = detect(str(img_path))
        results[img_path.name] = fruits

    with open(output_file_path, 'w') as ofp:
        json.dump(results, ofp)


if __name__ == '__main__':
    main()
