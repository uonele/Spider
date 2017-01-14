# coding:utf-8
from bs4 import BeautifulSoup
import requests
session = requests.session()
base_url = "http://172.18.254.101"
result_url = 'http://172.18.254.101/xs_main.aspx?xh=201416920411'
header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    # 我感觉这个cookie要自己程序来获取，不能设定为固定值。
    'Cookie': 'ASP.NET_SessionId=p1rcenmluy0o5muepysy0e55; BIGipServerpool-jw=1946030764.0.0000',
    'Host': '172.18.254.101',
    'Referer': 'http://172.18.254.101/xs_main.aspx?xh=201416920411',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

def login(account,password):
    user_type = '学生'
    bs = BeautifulSoup(session.get(base_url).content,'html.parser')
    __VIEWSTATE= bs.find('input',attrs={'name':'__VIEWSTATE'})['value']
    print __VIEWSTATE
    data = session.get(base_url+'/CheckCode.aspx').content
    with open('./autoCode.jpg','wb') as fb:
        fb.write(data)
    autoCode = raw_input("请输入验证码：")
    post = {
        '__VIEWSTATE' : __VIEWSTATE,
        'txtUserName':account,
        'TextBox2':password,
        'txtSecretCode':autoCode,
        'RadioButtonList1':user_type,
        'Button1':'',
        'lbLanguage':'',
        'hidPdrs':'',
        'hidsc':''
    }
    html2 = session.post(base_url + '/default2.aspx', post)
    html = BeautifulSoup(session.get(result_url).content, 'html.parser')
    return html.text
def getScore(account,password,str_):
    post = {
        'xh':account,
        'xm':password,
        'gnmkdm':str_
    }
    html = session.post(base_url + '/xscj.aspx', post)
    return html.text
def getPage():
    html = BeautifulSoup(session.get(result_url).content, 'html.parser')
    print html
if __name__ == '__main__':
    account = '2014169*****'
    password = '****'

    result1 = login(account,password)
    print result1




