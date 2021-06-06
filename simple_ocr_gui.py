# python3
# Create date: 2021-06-06
# Author: Scc_hy
# Func: 基于百度的开源OCR库进行文本识别的简单UI界面
# =================================================================================


from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QDesktopWidget
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QLabel, QMessageBox, QApplication
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtCore import Qt
from datetime import datetime
import os, sys
import re
from simple_chinese_ocr import pyqt5img_ocr, sample_ocr


class OcrUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.window_setting()
    
    def initUI(self):
        """
        主要功能
        """
        # 设置路径图像识别（第一优先级别）
        self.file_label = QLabel('输入文件名')
        self.file_label_Edit = QLineEdit()
        self.file_label_Edit.setPlaceholderText('输入需要进行中文识别的图片路径(可以为空)')

        # 设置剪切板图像识别
        self.pic_label = QPushButton('识别粘贴板/\n指定地址图片', self)
        self.pic_label.clicked.connect(self.pic2text)

        # 设置输出框
        self.ocr_Edit = QTextEdit()

        # 设置是否导出到文件，以及文件目录
        self.out_label = QPushButton('输出识别结果')
        self.out_label.clicked.connect(self.text2file)
        self.out_label_Edit = QLineEdit()
        self.out_label_Edit.setPlaceholderText('输入将文件输出的文件路径(如：./out.txt)')

        # 剪切板
        self.cb = QApplication.clipboard()

    def window_setting(self):
        """
        窗口位置摆放及简单装饰
        """
        # 摆放
        grid = QGridLayout()
        grid.setSpacing(16)

        grid.addWidget(self.file_label, 1, 0)
        grid.addWidget(self.file_label_Edit, 1, 1, 1, 3)
        grid.addWidget(self.pic_label, 2, 0)
        grid.addWidget(self.ocr_Edit, 2, 1, 2, 3)

        grid.addWidget(self.out_label, 4, 0)
        grid.addWidget(self.out_label_Edit, 4, 1, 1, 3)

        self.setLayout(grid)
        # 装饰
        self.set_decoration(self.file_label)
        self.set_decoration(self.file_label_Edit)
        self.set_decoration(self.pic_label)
        self.set_decoration(self.ocr_Edit)
        self.set_decoration(self.out_label)
        self.set_decoration(self.out_label_Edit)
        self.UI_gloabel_setting()

    def pic2text(self):
        """
        检查 self.file_label_Edit 中是否有文本
        如果有且存在该地址则有限检查改图片
        如果没有则在剪贴板中识别是否存在图片、存在则识别
        """
        now_ = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mdata = self.cb.mimeData()
        file_path = self.file_label_Edit.text()
        self.ocr_Edit.moveCursor(QTextCursor.End)
        if mdata.hasImage():
            a = self.cb.image()
            res = sample_ocr(file_path)  if self.__path_detect(file_path) else  pyqt5img_ocr(a)
            self.ocr_Edit.insertPlainText(f'{now_} | Image to detect: {str(res)}')
            self.edit_clear()
        elif self.__path_detect(file_path):
            res =  sample_ocr(file_path) 
            self.ocr_Edit.insertPlainText(f'{now_} | Image to detect: {str(res)}')
        else:
            self.ocr_Edit.insertPlainText(f'{now_} | No Image to detect')

    def text2file(self):
        res = self.ocr_Edit.toPlainText()
        partten = re.compile(r'\[.*?\]')
        out = re.findall(partten,  res)
        print('out :', out)
        out_file = self.out_label_Edit.text()
        if self.__path_detect(out_file):
            with open(out_file, 'a+') as f:
                f.write(''.join([i[1:-1] for i in out]))
            self.out_label_Edit.setText(f'wirte detect result to {out_file}')
        else:
            self.out_label_Edit.setText('No file to write result')


    def __path_detect(self, path_):
        if isinstance(path_, str):
            return os.path.exists(path_)
        return False

    def edit_clear(self):
        self.file_label_Edit.clear()

    def set_decoration(self, the_obj):
        font = QFont('Console', 12, QFont.Light)
        the_obj.setFont(font)


    # 其他的一些装饰
    def UI_gloabel_setting(self):
        """
        设置窗口大小 及 窗口置顶
        """
        self.setGeometry(300, 300, 650, 400)
        self.center()
        self.setWindowTitle('简单图片中文识别')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.show()
    
    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Exit',
                'Are you sure to quit?', QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def center(self):
        # 获取窗口
        qr = self.frameGeometry()
        # 获取屏幕中心
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OcrUI()
    sys.exit(app.exec_())