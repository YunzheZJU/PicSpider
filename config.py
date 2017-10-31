# -*- coding: utf-8 -*-

LOG_PATH = "log.log"
IMAGE_FOLDER_PATH = "images1"

KEYWORD = "抽象画"

REG_DETAILS = r'<a href="(.*?)"><img'
REG_IMAGE = r'<a href="(.*?)">原图'

MIN_NUM = 1
MAX_NUM = 1992
STEP = 60  # 60 is the maximum

# PROXIES = {
#     "http": "http://127.0.0.1:1997",
#     "https": "http://127.0.0.1:1997",
# }

TIMEOUT = 10
