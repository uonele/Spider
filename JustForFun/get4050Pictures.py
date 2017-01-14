# coding:utf-8
import requests
import os
class Pictures():
    def __init__(self):
        self.session = requests.session()
        self.base_url = "http://img.infinitynewtab.com/wallpaper/"
        self.base_dir_path = r'C:\Users\uonele\Pictures\bizhi\Pic_'
    # 创建文件，path为相应的文件路径
    def mkdirs(self, path):
        prefix = os.path.dirname(path)
        if not os.path.exists(prefix):
            os.makedirs(prefix)
    def getPics(self):
        for j in range(1,4050,50):
            base_dir_name = str(j)+'_' + str(j + 50)
            dir_path = self.base_dir_path + base_dir_name + '\\pic_'
            for i in range(j,j+50):
                file_name = str(i)+ '.jpg'
                file_path = dir_path + file_name
                self.mkdirs(file_path)
                data = self.session.get(self.base_url + file_name).content
                with open(file_path, 'wb') as fb:
                    fb.write(data)
                    print "generate Picture No."+str(i)
        print "you have got "+ str(4050)+"pictures in "+ self.base_dir_path
if __name__ == '__main__':
    pics = Pictures()
    pics.getPics()