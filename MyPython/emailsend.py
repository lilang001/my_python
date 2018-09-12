__author__ = 'Administrator'


from email.mime.text import MIMEText
import smtplib

try:
    msg = MIMEText('hello', 'plain', 'utf-8')

    from_addr = input('284507438@qq.com')

    password = input('')

    to_addr = input('lilang250@163.com')

    smtp_server = input('smtp.qq.com')


    server = smtplib.SMTP(smtp_server, 465)
    server.set_debuglevel(1)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally...')
print('END')
