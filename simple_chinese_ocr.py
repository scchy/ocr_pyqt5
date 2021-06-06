# python3
# Create date: 2021-06-06
# Author: Scc_hy
# Func: 基于百度的开源OCR库进行文本识别
# =================================================================================


import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import numpy as np
from PyQt5.QtGui import QImage
import time
from PIL import Image
import time
from paddleocr import PaddleOCR


ocr = PaddleOCR(lang='ch', use_gpu=False)
def sample_ocr(img:"np.array/os.path", ocr_model:"paddleocr.PaddleOCR"=ocr, show:bool=True) -> list:
    """
    基于百度开源的ocr库进行中文识别
    param img: np.array 图片矩阵 | os.path 图像目录
    param ocr_model: paddleocr.PaddleOCR 百度ocr模型
    param show: bool 是否将ocr识别的图片展示出来
    """
    if show:
        Image.fromarray(img).show()
    st = time.perf_counter()
    res = ocr_model.ocr(img, rec=True, det=True)
    cost_ = time.perf_counter() - st
    print(f'Finished detect the pic - {cost_:.5f}s')
    return [i[1][0] for i in res]


def pyqt5_img2arr(q_img: QImage) -> np.array:
    """
    将pyqt5的图片格式转换成np.array
    注: 直接转化的图片是4通道的，需要再借助PIL转化一下
    """
    # QImage -> np.array (m, n, 4)
    q_img = q_img.convertToFormat(QImage.Format_RGBA8888)
    width = q_img.width()
    height = q_img.height()
    ptr = q_img.bits()
    ptr.setsize(width * height * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    # np.array (m, n, 4) -> np.array (m, n, 3)
    return np.array(Image.fromarray(arr).convert('RGB'))


def pyqt5img_ocr(q_img: "QImage/os.path") -> list:
    """
    pyqt5_img2arr -> sample_ocr
    """
    if isinstance(q_img, str) and os.path.exists(q_img):
        return sample_ocr(q_img)
    return sample_ocr(pyqt5_img2arr(q_img))

