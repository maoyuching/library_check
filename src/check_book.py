# -*-coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json
import re

import requests
from lxml import etree

# ********************************************
marco_no_dict = {
    "普林斯顿微积分读本": "38516e4e5744765544796e33426677716b73513771413d3d",

    "vim practical ": "677a793069412f547979556c515231534d6c396154773d3d"
}

#设置服务器所需信息
#163邮箱服务器地址
mail_host = '***填写邮件服务器地址****'
#163用户名
mail_user = '*****'
#密码(部分邮箱为授权码)
mail_pass = '*******'
#邮件发送方邮箱地址
sender = '********'
#邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['********']
# ********************************************


def query_books(marco_no):
    '''
        reutrn the number of book can be borrowed , 0, 1, or any
    '''
    url = "http://210.35.251.243/opac/item.php?marc_no={}".format(marco_no)
    page = requests.get(url)
    #page.text is string
    html = etree.HTML(page.text)
    info_list = html.xpath('//table[@id="item"]//tr/td[last()-1]//text()')
    #info_list is element list
    books_state = [item.encode('utf-8').decode('utf-8') for item in info_list]
    #books_state is str list
    books_borrowable = books_state.count("可借")
    print(books_borrowable)
    return books_borrowable


def writeLog(status, detail):
    '''
        wirte log in query.log
    '''
    with open('query.log', mode='a+', encoding='utf-8') as f:
        f.write("****** {} ******\n".format(datetime.now()))
        f.write("       {}: {} \n".format(status, detail))


def sendMail(title, content):
    #设置email信息
    #邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    #邮件主题
    message['Subject'] = title
    #发送方信息
    message['From'] = sender
    #接受方信息
    message['To'] = receivers[0]

    try:
        smtpObj = smtplib.SMTP()
        #连接到服务器
        smtpObj.connect(mail_host, 25)
        #登录到服务器
        smtpObj.login(mail_user, mail_pass)
        #发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        #退出
        smtpObj.quit()
        writeLog("success", "send mail success")
    except smtplib.SMTPException as e:
        writeLog("fail", "fail when send mail ")


def main():

    for book in marco_no_dict.keys():
        book_remainder = query_books(marco_no_dict.get(book))
        if book_remainder > 0:
            status = "查询成功！"
            detail = "{} 有 {} 本可借".format(book, book_remainder)
            writeLog(status, detail)
            title = "《{}》可以在图书馆借到啦！".format(book)
            content = "《{}》有 {} 本 可以在图书馆借到".format(book, book_remainder)
            sendMail(title, content)
        else:
            status = "没有查到可借"
            detail = "{} 没有查询到".format(book)
            writeLog(status, detail)


if __name__ == "__main__":

    main()
