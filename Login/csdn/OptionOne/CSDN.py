# coding:utf-8
import os
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup as BS
from Logger import Logger


class CSDN():

    '# 模拟CSDN登陆'

    def __init__(self):
        self.loginURL = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'

        self.pagePath = "temp/csdn.html"  # 保存登陆后的网页

        self.log_name = 'logger'  # 日志名字
        self.log_path = 'temp/logger.log'  # 日志路径

        log = Logger(self.log_name,self.log_path)
        self.logger = log.createLogger()
        self.opener = self.getOpener()

    # 处理cookie
    def getOpener(self):
        cookiejar = cookielib.LWPCookieJar()
        handlers = urllib2.HTTPCookieProcessor(cookiejar)
        opener = urllib2.build_opener(handlers)
        return opener

    # 获得登录页面的代码
    def getBS(self,url,opener):
        html = opener.open(url).read()
        bs = BS(html,"html.parser")
        return bs

    # 获得隐藏字段：lt..每次都不一样，需先从首页get到
    def get_lt(self,bs):
        lt = bs.find("input",{'type':'hidden','name':'lt'}).get("value")
        return lt

    # 获得隐藏字段：execution
    def get_execution(self,bs):
        execution = bs.find("input",{'type':'hidden','name':'execution'}).get("value")
        return execution

    # 构造post的参数
    def getPostData(self,account,password,bs):
        # 发送的报文
        post_data = {
            'username':account,
            'password':password,
            'lt':self.get_lt(bs),
            'execution':self.get_execution(bs),
            '_eventId':'submit'}
        data = urllib.urlencode(post_data)
        return data

    # 将网页保存到本地
    def savePage(self, text, path):
        self.mkdirs(path)
        f = open(path, "w")
        f.write(text)
        f.close()
        self.logger.info("已将网页写到本地%s" % path)

    # 创建文件，path为相应的文件路径
    def mkdirs(self, path):
        prefix = os.path.dirname(path)
        if not os.path.exists(prefix):
            os.makedirs(prefix)

    # 发送请求
    def sendRequest(self, url, data={}):
        self.opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36")]
        # 模拟登录
        result = self.opener.open(url, data)

    # 模拟登陆
    def login(self, account, password):
        bs = self.getBS(self.loginURL,self.opener)
        post_data = self.getPostData(account, password,bs)
        self.sendRequest(self.loginURL, post_data)    # 致此登陆成功

    # 登陆成功后，传入URL即可打开网页
    def openURL(self,url):
        text = self.opener.open(url).read()
        self.savePage(text, self.pagePath)

if __name__=='__main__':
    account = 'uonele@163.com'              #CSDN账号，
    password = '××××××'                     # 密码
    url = "http://my.csdn.net/?ref=toolbar" # 查看个人信息的界面

    login = CSDN()
    login.login(account,password)
    login.openURL(url)
