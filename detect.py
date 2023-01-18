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

    def empty_callback(value):
        pass

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.medianBlur(img,5)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #done
    minhsv_y = np.array([23, 95, 105])
    maxhsv_y = np.array([32, 255, 255])
    maskhsv_y = cv2.inRange(img_hsv, minhsv_y, maxhsv_y)
    kernel = np.ones((25, 25), np.uint8)
    maskhsv_y = cv2.morphologyEx(maskhsv_y, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((29, 29), np.uint8)
    maskhsv_y = cv2.morphologyEx(maskhsv_y, cv2.MORPH_CLOSE, kernel)
    resulthsv = cv2.bitwise_and(img_hsv, img_hsv, mask=maskhsv_y)
    resulthsv_H = resulthsv[:, :, 0]
    resulthsv_H = cv2.medianBlur(resulthsv_H, 5)
    canny_mask_y = cv2.Canny(resulthsv_H, 15, 35);
    yellow_img = cv2.cvtColor(resulthsv, cv2.COLOR_HSV2BGR)

    dilated_y = cv2.dilate(canny_mask_y, (1, 1), iterations=20)
    (cnt_y, hierarchy) = cv2.findContours(
        canny_mask_y.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #done
    minhsv_g = np.array([33, 50, 50])
    maxhsv_g = np.array([60, 255, 255])
    maskhsv_g = cv2.inRange(img_hsv, minhsv_g, maxhsv_g)
    kernel = np.ones((31, 31), np.uint8)
    maskhsv_g = cv2.morphologyEx(maskhsv_g, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((29, 29), np.uint8)
    maskhsv_g = cv2.morphologyEx(maskhsv_g, cv2.MORPH_CLOSE, kernel)
    resulthsv = cv2.bitwise_and(img_hsv, img_hsv, mask=maskhsv_g)
    resulthsv_H = resulthsv[:, :, 0]
    resulthsv_H = cv2.medianBlur(resulthsv_H, 15)
    canny_mask_g = cv2.Canny(resulthsv_H, 0, 15);
    kernel = np.ones((1, 1), np.uint8)
    canny_mask_g = cv2.morphologyEx(canny_mask_g, cv2.MORPH_OPEN, kernel)
    green_img = cv2.cvtColor(resulthsv, cv2.COLOR_HSV2BGR)

    dilated_g = cv2.dilate(canny_mask_g, (1, 1), iterations=20)
    (cnt_g, hierarchy) = cv2.findContours(
        canny_mask_y.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    minhsv_p = np.array([125, 25, 25])
    maxhsv_p = np.array([170, 255, 255])
    maskhsv_p = cv2.inRange(img_hsv, minhsv_p, maxhsv_p)
    kernel = np.ones((25, 25), np.uint8)
    maskhsv_p = cv2.morphologyEx(maskhsv_p, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((29, 29), np.uint8)
    maskhsv_p = cv2.morphologyEx(maskhsv_p, cv2.MORPH_CLOSE, kernel)
    resulthsv = cv2.bitwise_and(img_hsv, img_hsv, mask=maskhsv_p)
    resulthsv_H = resulthsv[:, :, 0]
    resulthsv_H = cv2.medianBlur(resulthsv_H, 5)
    canny_mask_p = cv2.Canny(resulthsv_H, 15, 35);
    purple_img = cv2.cvtColor(resulthsv, cv2.COLOR_HSV2BGR)

    dilated_p = cv2.dilate(canny_mask_p, (1, 1), iterations=20)
    (cnt_p, hierarchy) = cv2.findContours(
        canny_mask_p.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    minhsv_r = np.array([173, 35, 75])
    maxhsv_r = np.array([179, 255, 255])
    maskhsv1 = cv2.inRange(img_hsv, minhsv_r, maxhsv_r)
    minhsv_r = np.array([0, 35, 75])
    maxhsv_r = np.array([12, 255, 255])
    maskhsv2 = cv2.inRange(img_hsv, minhsv_r, maxhsv_r)
    maskhsv_r = cv2.bitwise_or(maskhsv1, maskhsv2)
    kernel = np.ones((25, 25), np.uint8)
    maskhsv_r = cv2.morphologyEx(maskhsv_r, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((5, 5), np.uint8)
    maskhsv_r = cv2.morphologyEx(maskhsv_r, cv2.MORPH_CLOSE, kernel)
    resulthsv = cv2.bitwise_and(img_hsv, img_hsv, mask=maskhsv_r)
    resulthsv_H = resulthsv[:, :, 0]
    resulthsv_H = cv2.medianBlur(resulthsv_H, 35)
    canny_mask_r = cv2.Canny(resulthsv_H, 0, 85);
    red_img = cv2.cvtColor(resulthsv, cv2.COLOR_HSV2BGR)

    dilated_r = cv2.dilate(canny_mask_r, (1, 1), iterations=5)
    (cnt_r, hierarchy) = cv2.findContours(
        canny_mask_r.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    red = len(cnt_r)
    yellow = len(cnt_y)
    green = len(cnt_g)
    purple = len(cnt_p)

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
