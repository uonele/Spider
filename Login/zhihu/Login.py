# coding:utf-8
import os
import urllib
import urllib2
import cookielib
import re
import json
from Logger import Logger
from bs4 import BeautifulSoup as BS

class Login():
    """
    模拟登陆知乎
    by uonele
    2016/12/16
    """
    def __init__(self):
        self.log_name = 'logger'                                            # 日志名字
        self.log_path = 'temp/logger.log'                                  # 日志路径
        self.pagePath = "temp/zhihu.html"                                  # 保存登陆后的网页
        self.captchaPath = 'temp/captcha.jpg'                              # 保存验证码
        self.baseURL = "https://www.zhihu.com/"                            # 首页，需
        self.loginURL = "https://www.zhihu.com/login/phone_num"            # 手机号登陆（如是邮箱登陆，则将后面的phone_num替换成email）
        self.captchaURL = "https://www.zhihu.com/captcha.gif?type=login"   # 请求验证码页面
        log = Logger(self.log_name,self.log_path)
        self.logger = log.createLogger()
        self.opener = self.getOpener()
        urllib2.install_opener(self.opener)
        self.header = {                                                     # 头部
            'Accept':'*/*' ,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'Referer':'https://www.zhihu.com/',
            'Accept-Language':'en-GB,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Accept-Encoding':'gzip, deflate, br',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'Host':'www.zhihu.com'}
    # 处理cookie
    def getOpener(self):
        cookiejar = cookielib.LWPCookieJar()
        handlers = urllib2.HTTPCookieProcessor(cookiejar)
        opener = urllib2.build_opener(handlers)
        return opener

    # 获取验证码必给你保存到本地
    def saveCaptcha(self,captchaURL,captchaPath):
        self.mkdirs(captchaPath)
        pic = self.opener.open(captchaURL).read()
        f = open(self.captchaPath,"wb")
        f.write(pic)
        f.close()
        self.logger.info("已将验证码写到本地" )

    # 表单中隐藏的一个字段，每次都不一样，需先从首页get到
    def get_xsrf(self,url):
        html = self.opener.open(url).read()
        bs = BS(html,"html.parser")
        _xsrf = bs.find("input",{'type':'hidden'}).get("value")
        return _xsrf

    # 构造post的参数
    def getPostData(self,account,password):
        _xsrf = self.get_xsrf(self.baseURL)
        captcha = raw_input("输入验证码：")
        # 发送的报文
        self.post_data = {
            '_xsrf': _xsrf,                             # 在网页中是个隐藏的表单字段，可从源码提取出
            'phone_num': account,                       # 如果是email登陆，则key为“email”
            'password': password,
            'remember_me': 'true',
            'captcha':captcha
        }

    def sendRequest(self,url,data={},header={}):
        '''
        发送请求并解析响应

        报文发送后返回一个result，是个json数据：
            如登陆成功：则result为：
                {   "r":0,
                    "msg": "\u767b\u5f55\u6210\u529f"
                }
                解析后如下：
                    {u'msg': u'\u767b\u5f55\u6210\u529f', u'r': 0}
            如登陆失败：则result为：
                {
                    "r": 1,
                    "errcode": 100005,
                    "data": {"password":"\u5e10\u53f7\u6216\u5bc6\u7801\u9519\u8bef"},
                    "msg": "\u5e10\u53f7\u6216\u5bc6\u7801\u9519\u8bef"
                }
                解析后如下：
                {u'msg': u'\u5e10\u53f7\u6216\u5bc6\u7801\u9519\u8bef', u'r': 1, u'data': {u'password': u'\u5e10\u53f7\u6216\u5bc6\u7801\u9519\u8bef'}, u'errcode': 100005}
        '''
        request = urllib2.Request(url, urllib.urlencode(data), header)
        result = urllib2.urlopen(request)
        resText = result.read()
        jsonText = json.loads(resText)
        if jsonText["r"] == 0:
            self.logger.info("知乎模拟登陆成功。")
        else:
            self.logger.error("登陆失败")

    # 将网页保存到本地
    def savePage(self,text,path):
        self.mkdirs(path)
        f = open(path,"w")
        f.write(text)
        f.close()
        self.logger.info("已将网页写到本地")

    # 创建文件，path为相应的文件路径
    def mkdirs(self,path):
        prefix = os.path.dirname(path)
        if not os.path.exists(prefix):
            os.makedirs(prefix)

    # 模拟登陆
    def login(self, account, password):
        self.saveCaptcha(self.captchaURL, self.captchaPath)
        self.getPostData(account, password)
        self.sendRequest(self.loginURL, self.post_data, self.header)    # 致此登陆成功
        text = self.opener.open(self.baseURL).read()                    # 重新打开主页，内容即为登陆后看到的内容
        self.savePage(text, self.pagePath)
if __name__=='__main__':
    account = '13027629892'         # 知乎账号，此处填写手机号
    password = '********'         # 密码
    login = Login()
    login.login(account,password)
