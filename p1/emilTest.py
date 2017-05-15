from email.mime.text import MIMEText
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sendEmil(count):
    # 输入Email地址和口令:
    from_addr = '@qq.com'
    password = ''  # 授权码 qq邮箱那个。在设置里面发短信获取
    # 输入收件人地址:
    to_addr = '@163.com'
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'

    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr('我是发件人 <%s>' % from_addr)
    msg['To'] = _format_addr('收件人 <%s>' % to_addr)
    msg['Subject'] = Header('我是标题……%s' % count, 'utf-8').encode()

    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


for i in range(100):
    sendEmil(i)
