# coding:utf-8
import logging
import os
class Logger():
    def __init__(self,log_name,log_path):
        self.log_name = log_name
        self.log_path = log_path
    # 创建日志文件
    def createLogger(self):
        self.mkdirs(self.log_path)
        logger = logging.getLogger(self.log_name)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')   # 预定义日志格式
        # 创建一个操作句柄，指向具体写入的文件
        file_handler = logging.FileHandler(self.log_path)
        stream_handler = logging.StreamHandler()        # 用于输出到控制台
        # 格式化句柄
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        # 将句柄添加到日志操作中
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        return logger

    #创建文件，path为相应的文件路径
    def mkdirs(self,path):
        file = os.path.dirname(path)
        if not os.path.exists(file):
            os.makedirs(file)