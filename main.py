# -*- coding: utf-8 -*-
import os
import re
import urllib
import requests
from logger import logger
from config import KEYWORD, REG_DETAILS, REG_IMAGE, MIN_NUM, MAX_NUM, STEP, IMAGE_FOLDER_PATH, PROXIES, TIMEOUT


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_resp(session, url, stream=False):
    logger.info("Waiting for " + url)
    if stream:
        resp = session.get(url, stream=stream, proxies=PROXIES, timeout=TIMEOUT)
    else:
        resp = session.get(url, proxies=PROXIES, timeout=TIMEOUT)
    return resp


def write_img(file_path, response):
    with open(file_path, "wb") as img_file:
        for chunk in response.iter_content(chunk_size=1024):
            img_file.write(chunk)
            img_file.flush()
    logger.info("Written successfully.")


def get_result_img(session, result):
    if result:
        img_url = result.group(1)
        write_img(os.path.join(IMAGE_FOLDER_PATH, img_url.split("/")[-1]),
                  get_resp(session, img_url, stream=True))


def jump_into_details(session, paths, reg):
    for path in paths:
        resp = get_resp(session, "http://image.baidu.com" + path)
        result_image = reg.search(resp.content)
        get_result_img(session, result_image)


def process_this_page(session, url, reg_details, reg_image):
    resp = get_resp(session, url)
    list_detail_paths = reg_details.findall(resp.content)
    if list_detail_paths:
        jump_into_details(session, list_detail_paths, reg_image)


def pic_spider():
    # Create Folder
    make_dir(IMAGE_FOLDER_PATH)

    # Create Session
    session = requests.session()

    # Compile Regs
    reg_details = re.compile(REG_DETAILS)
    reg_image = re.compile(REG_IMAGE)

    # Main Loop
    for np in range(MIN_NUM, MAX_NUM, STEP):
        try:
            detail_url = "http://image.baidu.com/search/wisemidresult?tn=wisemidresult&ie=utf8" \
                         + "&word=" + urllib.quote(KEYWORD) \
                         + "&pn=" + str(np) \
                         + "&rn=" + str(STEP)
            process_this_page(session, detail_url, reg_details, reg_image)
        except StandardError, e:
            logger.error(e)


if __name__ == '__main__':
    try:
        pic_spider()
    except Exception, e:
        logger.error(e)
