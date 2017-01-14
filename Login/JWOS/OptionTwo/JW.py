#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
import cookielib

class JWOS:
    def __init__(self):
        self.ImageUrl = 'http://172.18.254.101/CheckCode.aspx'
        self.LoginUrl = 'http://172.18.254.101/default2.aspx'
        self.cookies = cookielib.CookieJar()
        self.handles = urllib2.HTTPCookieProcessor(self.cookies)
        self.opener = urllib2.build_opener(self.handles)
        self.headers={
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Connection':'keep-alive',
                    #'Content-Length':'194',
                    #'Content - Type': 'application / x - www - form - urlencoded',
                    #'Host':'172.18.254.101',
                    #'Origin':'http://172.18.254.101',
                    'Referer':'http://172.18.254.101/default2.aspx',
                    #'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    def saveImage(self,code):
        imagePath = open('./Image.jpg','wb')
        imagePath.write(code)
        imagePath.close()
    def getCheckCode(self):
        picture = self.opener.open(self.ImageUrl)
        self.saveImage(picture.read())
    def getPage(self,inputCheckCode):
        postData={
                  '__VIEWSTATE':'dDwyODE2NTM0OTg7Oz5oXHiwqruyxtrLZJG28i4AOKLFhg==',
                  'txtUserName':'201416920411',
                  'TextBox2':'wwl19961218',
                  'txtSecretCode':inputCheckCode,
                  'RadioButtonList1':'学生',
                  'Button1':'',
                  'lbLanguage':'',
                  'hidPdrs':'',
                  'hidsc':''
        }
        data = urllib.urlencode(postData)
        request = urllib2.Request(url=self.LoginUrl,data=data,headers=self.headers)
        try:
            response = self.opener.open(request)
            result  = response.read().decode('gb2312')
            print result
        except urllib2.HTTPError,e:
            if hasattr(e,'code'):
                print e.code
            if hasattr(e,'reason'):
                print e.reason

    def start(self):
        self.getCheckCode()
        checkCode = raw_input('请输入验证码:\n')
        checkCode.strip()
        self.getPage(checkCode)
if __name__ == '__main__':
    JW = JWOS()
    JW.start()